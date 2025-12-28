import sys, os, textwrap, config, subprocess, re
from langchain_openai import ChatOpenAI
from langchain_neo4j import Neo4jGraph, GraphCypherQAChain
from langchain_core.prompts import PromptTemplate

llm = ChatOpenAI(
    model="gpt-5.2", 
    temperature=0,
    openai_api_key=config.OPENAI_API_KEY,
)

graph = Neo4jGraph(
    url=config.NEO4J_URI,
    username=config.NEO4J_USER,
    password=config.NEO4J_PASSWORD,
)

CYPHER_GENERATION_TEMPLATE = """
    あなたは、CADアプリケーション「EvoShip」のAPIに関する知識グラフを熟知したエキスパートです。
    ユーザーの質問を解釈し、提供されたグラフスキーマ情報に基づいて、その答えを見つけるための最適なCypherクエリを生成するタスクを担います。

    ## グラフスキーマ情報
    以下に、利用可能なノードラベル、プロパティ、およびリレーションシップタイプの情報を示します。クエリは**必ずこのスキーマ情報に厳密に従って**生成してください。
    {schema}

    ## クエリ生成の指示
    1.  **思考プロセスに従う:** 以下の思考プロセスに従って、最適なクエリを段階的に構築してください。
        -   **Step 1. 意図の理解:** ユーザーが「何を知りたいのか」「何をしたいのか」という根本的な意図を特定します。(例: APIの使い方を知りたい、サンプルコードが欲しい、概念を理解したい、既存コードを修正したい)
        -   **Step 2. キーワード抽出:** 質問から重要なキーワード（API名、操作対象、目的、修正内容など）を抽出します。
        -   **Step 3. スキーマとのマッピング:** 抽出したキーワードを**上記のグラフスキーマ情報**と照らし合わせます。検索の起点となるノードラベル (`Method`, `ScriptExample`等)、検索対象のプロパティ (`name`, `description`, `summary`等)、たどるべきリレーションシップタイプ (`IS_EXAMPLE_OF`, `HAS_PARAMETER`等) を慎重に選択します。スキーマに存在しない要素は絶対に使用しないでください。
        -   **Step 4. クエリ生成:** 上記の考察に基づき、最終的なCypherクエリを生成します。キーワード検索には `toLower()` と `CONTAINS` を活用し、できるだけ多くの関連情報を取得できるよう努めてください。ヒットしない場合は、検索条件を緩和する（例：ANDをORにする、検索対象プロパティを増やす）ことも検討してください。

    2.  **検索戦略のヒント:**
        -   **「方法」「やり方」** に関する質問には、`Method`ノードの `description` や `ScriptExample`ノードの `summary` を検索するのが有効です。
        -   **「サンプルコード」「実装例」** に関する質問には、`ScriptExample`ノードを起点とし、`IS_EXAMPLE_OF`リレーションで関連する`Method`を探します。`ScriptExample`ノードには`code`プロパティにコード全文が格納されています。
        -   **概念や機能**に関する質問には、`Entity` ノードを検索するのが有効です。
        -   質問に複数のキーワードが含まれる場合、それらが異なるノードのプロパティにマッチする可能性を考慮してください。例えば、「プレートを作成するAPIの引数」という質問では、「プレート」「作成」が`Method`や`ScriptExample`に、「引数」が`Parameter`ノードに関連する可能性があります。

    ## Few-shot Examples (質問とクエリの例)
    -   **質問:** 「プレートを作成するサンプルコードはありますか？」
    -   **Cypherクエリ:**
        ```cypher
        MATCH (s:ScriptExample)-[:IS_EXAMPLE_OF]->(m:Method)
        WHERE (toLower(s.summary) CONTAINS 'プレート' AND toLower(s.summary) CONTAINS '作成')
        OR (toLower(m.description) CONTAINS 'プレート' AND toLower(m.description) CONTAINS '作成')
        RETURN s.name AS script_name, s.code AS script_code, s.summary AS script_summary
        ```
    -   **質問:** 「点群を扱うAPIには何がありますか？」
    -   **Cypherクエリ:**
        ```cypher
        MATCH (m:Method)-[:HAS_PARAMETER|HAS_RETURNS]->(:Parameter|ReturnValue)-[:HAS_TYPE]->(t:DataType)
        WHERE toLower(t.name) CONTAINS '点'
        RETURN DISTINCT m.name AS method_name, m.description AS method_description
        ```
    ## 出力要件
    -   生成されたCypherクエリのみを、` ```cypher ... ``` ` のようなコードブロックなしで、**文字列としてそのまま出力してください。**
    -   説明、前置き、括弧、謝罪は一切含めないでください。
    -   **クエリは必ず `MATCH` や `RETURN` などのキーワードから開始してください。**
    ---
    **質問:** {question}
    **Cypherクエリ:**
    """

CYPHER_GENERATION_PROMPT = PromptTemplate(
    input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
)

QA_TEMPLATE = """
    あなたは、CADアプリケーション「EvoShip」をPythonで操作するエキスパートです。
    あなたのタスクは、ユーザーの要求とナレッジグラフから取得した情報を基に、単一の完成された実行可能なPythonスクリプトと、そのスクリプトに関する説明を生成することです。

    ユーザーの要求:
    {question}

    ナレッジグラフから取得した関連情報:
    {context}

    上記の情報を基に、以下の要件と出力形式に従って回答を生成してください。

    ## スクリプト生成の要件
    - **ユーザーの要求に「元のスクリプト」が含まれる場合は、それを基に編集・修正を行ってください。**
    - **「元のスクリプト」が含まれない場合は、ゼロから新しいスクリプトを作成してください。**
    - 新規作成の場合は、常に `import win32com.client` から始めること。
    - 新規作成の場合は、アプリケーションを起動する定型コード `evoship = win32com.client.DispatchEx("EvoShip.Application")` を含めること。
    - 新規作成の場合は、ドキュメントとパートを作成するコード `doc = evoship.Create3DDocument()` と `part = doc.GetPart()` を含めること。
    - メソッドの返り値は、後続のメソッドで利用するために変数に格納すること。
    - 複数のAPI呼び出しがある場合、それらを論理的な順序で構成すること。
    - 取得した情報から最も適切と考えられる単一のスクリプトを作成すること。
    - ナレッジグラフからの情報にサンプルコードが含まれている場合は、それを最優先で参考にし、必要に応じて質問内容に合わせて修正してください。

    ## 出力形式
    以下のマークダウン形式で回答してください。コードや説明以外の余計な文章は含めないでください。

    ## 生成されたスクリリプト
    ```python
    # ここにPythonスクリプトを記述
    ````

    ### スクリプトの説明

    ここに、生成したスクリプトが何をするものか、使用されている主要なAPIの目的、そしてユーザーが注意すべき点などを簡潔に解説してください。
    """

QA_PROMPT = PromptTemplate(
input_variables=["context", "question"], template=QA_TEMPLATE
)

graph_qa = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    verbose=True,
    cypher_prompt=CYPHER_GENERATION_PROMPT,
    qa_prompt=QA_PROMPT,
    allow_dangerous_requests=True,
    top_k=10000,
)


FIX_TEMPLATE = """
    あなたはPythonコードの修正を行うエキスパートです。
    以下のコードを実行したところ、エラーが発生しました。
    エラーメッセージと元のコードを分析し、エラーを修正した完全なPythonコードを生成してください。

    ## 元のコード
    ```python
    {code}
    ```

    ## エラーメッセージ
    {error}

    ## 修正の指示
    - エラーの原因を特定し、修正してください。
    - 修正後のコードのみを以下の形式で出力してください。
    - 説明は最小限に留めてください。

    ```python
    # 修正後のコード
    ```
"""

FIX_PROMPT = PromptTemplate(
    input_variables=["code", "error"], template=FIX_TEMPLATE
)

def run_script(script_path: str) -> tuple[bool, str]:
    """
    スクリプトを実行し、成功したかどうかと出力（またはエラー）を返します。
    戻り値: (success: bool, message: str)
    """
    print(f"--- Executing script: {script_path} ---")
    try:
        # タイムアウトを設定して無限ループなどを防止（例: 30秒）
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except subprocess.TimeoutExpired:
        return False, "Error: Script execution timed out."
    except Exception as e:
        return False, f"Error executing script: {str(e)}"

def fix_code(code: str, error_message: str) -> str:
    """
    エラー情報を元にLLMに修正を依頼します。
    """
    print("--- Requesting fix from LLM ---")
    prompt = FIX_PROMPT.format(code=code, error=error_message)
    response = llm.invoke(prompt)
    
    return response.content

def ask(question: str, original_code: str = None) -> str:
    """
    Neo4jグラフ検索を用いて質問に回答します。
    original_codeが指定された場合は、それを編集するタスクとして扱います。
    """

    final_question = f"""
    以下の【元のスクリプト】を【編集指示】に従って修正してください。
    【元のスクリプト】
    ```python
    {original_code}
    【編集指示】
    {question}
    """

    print("--- Running Graph Search (Neo4j) ---")
    # グラフ検索の実行
    result = graph_qa.invoke({"query": final_question})
    return result['result']

if __name__ == "__main__": 
    import argparse 
    import re

    parser = argparse.ArgumentParser(
        description="Edit Python scripts for EvoShip using GraphRAG (Neo4j).", # 説明文を修正
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=textwrap.dedent(__doc__ or"")
    )
    
    # 引数定義を変更: 第一引数を明確に file_path とし、instruction を必須にする
    parser.add_argument(
        "file_path", 
        help="The path to the existing Python script to edit."
    )
    parser.add_argument(
        "instruction", 
        # nargs='?', を削除して必須引数にする
        help="The editing instruction."
    )
    
    parser.add_argument(
        "-o", "--output", 
        help="The file path to save the generated Python script."
    )

    args = parser.parse_args()

    # --- 引数の解析とファイルの読み込み (編集モードのみ) ---
    file_path = args.file_path
    question = args.instruction
    original_code = None

    if not os.path.exists(file_path):
        print(f"エラー: 指定されたファイル '{file_path}' が見つかりません。")
        sys.exit(1)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_code = f.read()
        print(f"--- [Mode: Edit] Loading script from: {file_path} ---")
    except Exception as e:
        print(f"エラー: ファイル '{file_path}' の読み込み中にエラーが発生しました: {e}")
        sys.exit(1)

    # --- 実行 ---
    try:
        MAX_RETRIES = 3
        current_code = None
        error_output = None 
        
        for attempt in range(MAX_RETRIES + 1):
            if attempt == 0:
                # 初回生成 (original_codeを必ず渡す)
                answer = ask(question, original_code=original_code)
            else:
                # 修正ループ
                print(f"\n=== Self-Correction Attempt {attempt}/{MAX_RETRIES} ===")
                answer = fix_code(current_code, error_output)

            # --- 以下、出力処理・実行ロジックは変更なし ---
            script_code = None
            
            if args.output:
                # スクリプト部分を正規表現で抽出
                script_match = re.search(r"```python\n(.*?)```", answer, re.DOTALL)
                if script_match:
                    script_code = script_match.group(1).strip()
                    current_code = script_code 
                    
                    with open(args.output, 'w', encoding='utf-8') as f:
                        f.write(script_code)
                    print(f"\n--- Script saved to: {args.output} ---")

                    explanation_match = re.search(r"### スクリプトの説明\n\n(.*)", answer, re.DOTALL)
                    if explanation_match:
                        explanation = explanation_match.group(1).strip()
                        print("\n--- Script Explanation ---")
                        print(explanation)
                    
                    success, output = run_script(args.output)
                    
                    if success:
                        print("\n--- Execution Successful ---")
                        print(output)
                        break 
                    else:
                        print(f"\n--- Execution Failed (Attempt {attempt+1}) ---")
                        print(output)
                        error_output = output 
                        
                        if attempt == MAX_RETRIES:
                            print("\n--- Max retries reached. Giving up. ---")
                else:
                    print("\n--- Generated Answer (script not found) ---")
                    print(answer)
                    break 
            else:
                print("\n--- Generated Answer ---")
                print(answer)
                break

    except ValueError as e:
        print(f"\nエラー: {e}")
    except Exception as e:
        print(f"\n予期せぬエラーが発生しました: {e}")
    