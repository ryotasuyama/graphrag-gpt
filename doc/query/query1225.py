"""
使い方:

[参考スクリプトの指定]
    python query1225.py ./script/sample_no_bracket.py "ブラケットをつけてください。" --reference ./script/samplename.py -o ./script/1225-1.py

[出力先の指定]
    python query1225.py <ファイルパス> "<編集指示>" -o ./output/result.py

[デフォルトの動作]
- 検索方法はグラフ検索のみです。
    例: python query1225.py <ファイルパス> "<編集指示>"
- 出力先を指定しない場合は、標準出力に結果が表示されます。
"""
import sys, os, textwrap, config, re
# --- [変更点] 必要なモジュールを更新 ---
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
# RetrievalQA は削除し、新しいチェーン作成関数をインポート
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

from langchain_neo4j import Neo4jGraph, GraphCypherQAChain
from langchain_core.prompts import PromptTemplate
from neo4j.exceptions import ClientError, CypherSyntaxError

# ---------- 共通 LLM ----------
llm = ChatOpenAI(
    model="gpt-5.2", 
    temperature=0,
    openai_api_key=config.OPENAI_API_KEY,
)

# ---------- Vector QA (Updated) ----------
vectordb = Chroma(
    persist_directory="data/chroma_db",
    embedding_function=OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY),
)

# --- [変更点] create_retrieval_chain への移行 ---
# 1. 回答生成用のプロンプトテンプレートを定義
qa_system_prompt = (
    "あなたはCADアプリケーション「EvoShip」のAPI操作コードを生成するアシスタントです。\n"
    "以下の検索されたコンテキスト情報を使用して、ユーザーの質問に答えてください。\n"
    "**重要: スクリプトは必ず最後まで完全に生成してください。途中で終了したり、「続きます」「省略」「この後も...」などのコメントを追加したりしないでください。**\n"
    "回答のみを出力してください。\n\n"
    "{context}"
)
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        ("human", "{input}"),
    ]
)

# 2. ドキュメント結合チェーン (Stuff chain) の作成
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

# 3. 検索チェーン (Retrieval chain) の作成
vector_qa_chain = create_retrieval_chain(vectordb.as_retriever(), question_answer_chain)
# -----------------------------------------------

# ---------- Graph QA ----------
graph = Neo4jGraph(
    url=config.NEO4J_URI,
    username=config.NEO4J_USER,
    password=config.NEO4J_PASSWORD,
)

CYPHER_GENERATION_TEMPLATE_JP = """
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
    input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE_JP
)

QA_TEMPLATE = """
    あなたは、CADアプリケーション「EvoShip」をPythonで操作するエキスパートです。
    あなたのタスクは、ユーザーの要求とナレッジグラフから取得した情報を基に、単一の完成された実行可能なPythonスクリプトと、そのスクリプトに関する説明を生成することです。

    ユーザーの要求:
    {question}

    ナレッジグラフから取得した関連情報:
    {context}

    上記の情報を基に、以下の「参考スクリプトの分析指針」に従って、最適なスクリプトを生成してください。

    ## 参考スクリプトの分析・適用指針
    参考スクリプトが提供されている場合、以下の3点を徹底的に分析し、修正後のスクリプトに反映してください：
    1. **接続対象（Target Members）の特定:**
       - ブラケットが「どの部材（例：Plate, Stiffener, Longitudinal, Girder）」に対して取り付けられているか、その組み合わせを抽出してください。
       - 取り付け位置（StartPoint, EndPoint, Intersectionなど）の計算ロジックを正確に読み取ってください。
       - ブラケットは Surfaces1 / Surfaces2 の "面ペア" で定義される点に注意し、参照面の型（PLS と FL/WF/WB）を抽出すること。
       - 代表的なペアは (板PLS×Profile FL) と (Profile FL×Profile FL)。板PLSは solidX または profileXX[1] を参照する場合がある。
       - ブラケットの BaseElement は原則 Profile（profileXX[0]）。ブラケット候補は AddAttachSurfaces を持ち、End1/End2 が定義されているスティフナ（ProfileType 1002/1003 など）を優先すること。
    2. **パラメータの依存関係（Parameter Logic）:**
       - ブラケットのサイズ（Height, Width, Thickness）が、接続先の部材サイズや属性からどのように算出されているかを確認してください。
       - ブラケットの種類（Type）や向き（Orientation/Vector）を決定するパラメータの組み合わせパターンを模倣してください。
       - 参考スクリプトに BracketType（例: 1501/1505）や Sf1EndElements/Sf2EndElements がある場合は必ず踏襲すること。
    3. **配置の完全性とエラー回避:**
       - 複数の箇所にブラケットが必要な場合、ループ処理や条件分岐がどのように行われているかを確認し、修正対象のスクリプトでも「漏れなく」配置されるようにしてください。
       - API呼び出しの前に必要な初期化処理や、戻り値の型チェックが参考スクリプトで行われている場合、それを必ず継承してください。

    ## ブラケット生成のドメインルール（既存スクリプト実績に合わせる）

    ### 1) ブラケットの基本構造（必ず守る）
    - ブラケットは「2つの面（Surfaces1 / Surfaces2）」を結ぶ要素として定義する。
    - ブラケットの起点（BaseElement）は原則として Profile 部材（例: profileXX[0]）を使う。
    - Surfaces は "面の参照" を配列で指定する。参照の典型は次のいずれか：
      - Plate面（板）：["PLS", <offset等>, solidX] または ["PLS", <offset等>, profileXX[1]]
      - Profile面（断面材）：profileXX[0] + ",FL"（基本）／必要時のみ ",WF" ",WB" を使用

    ### 2) 代表的な接続ペア（優先順に探索して追加）
    次のペアが見つかったらブラケット候補として扱い、可能なら複数箇所に漏れなく配置する。

    (A) Plate（Solid の PLS 面） × Stiffener（Profile の FL 面）
    - 例：Surfaces1 = ["PLS", ..., solid1/2/3/4]、Surfaces2 = [profileYY[0] + ",FL"]
    - BracketType は Plate×Profile 用の既存スクリプトの型（例: 1505）があるならそれを踏襲する。

    (B) Stiffener（Profile の FL 面） × Stiffener（Profile の FL 面）
    - 例：Surfaces1 = [profileAA[0] + ",FL"]、Surfaces2 = [profileBB[0] + ",FL"]
    - BracketType は Profile×Profile 用の既存スクリプトの型（例: 1501）があるならそれを踏襲する。

    (C) "Profile が持つ板要素"（profileXX[1] の PLS 面）× Plate（Solid の PLS 面） or 板×板
    - 例：Surfaces1 = ["PLS", ..., profileAA[1]]、Surfaces2 = ["PLS", ..., solidX]（または profileBB[1]）
    - このケースが出るモデルでは BracketType=1501 系が使われることがあるため、参考スクリプトの型・フィールドを優先する。

    ### 3) ブラケットを付けられる「部材側の特徴」を使って候補抽出
    ブラケット候補の BaseElement（主役Profile）は次の特徴を満たすものを優先して選ぶ：
    - AddAttachSurfaces(...) で板に取り付いている（= "板付きスティフナ"）
    - 端部が決まっている：AddEnd1Elements(...) / AddEnd2Elements(...) が存在する
    - 面ラベルが参照可能：特に ",FL" を持つ断面材が主対象
    - ProfileType がスティフナ系（例: 1002 / 1003）なら優先。複合型（例: 1201）で profile[1] を持つ場合は (C) の候補にもできる。

    ### 4) 配置位置の決め方（参考スクリプトが無い場合のデフォルト戦略）
    - 可能なら「各スティフナの End1 / End2 付近」にブラケットを入れる（端部要素があるなら、その接続相手側に向ける）。
    - Sf1EndElements / Sf2EndElements が参考例に存在する場合は必ず模倣し、ブラケットの適用範囲（端部側）を明確化する。
    - 具体的な点計算や交点計算が元スクリプトにある場合は、それを流用し、座標系・方向ベクトル・オフセットの定義を変えない。

    ### 5) 生成時の安全策（壊さない）
    - ブラケット生成コードは、対象となる部材（solid/profile）が全て生成された後に追加する。
    - 変数名は衝突させない（例: bracket_param_###, bracket_###）。
    - APIの戻り値が None の可能性がある場合は、参考スクリプトの流儀に合わせてガードする。
    - BracketType / 各フィールドは "参考スクリプトまたはナレッジグラフのサンプル" で確認できる値を最優先し、未知のフィールドを勝手に追加しない。

    ## スクリプト生成の要件
    - **元のスクリプトを基に編集・修正を行ってください。**
    - **「参考スクリプト」が提供されている場合は、その構造、APIの使用方法、コーディングスタイルを参考にしながらスクリプトを編集してください。**
    - **【最重要】スクリプトは必ず最後まで完全に生成してください。元のスクリプトの全長を維持し、編集指示に関係する部分だけでなく、元のスクリプトのすべてのコードを含めてください。**
    - **【禁止事項】以下のようなコメントや説明をコード内に追加しないでください：**
      - 「この後も続きます」「省略」「...」「この後も元スクリプトと同様に...」などの途中終了を示すコメント
      - 「上記3箇所の...」のような部分的な説明コメント
      - 「実運用では...」「注意: 実運用では...」のような注意書きコメント
    - メソッドの返り値は、後続のメソッドで利用するために変数に格納すること。
    - 複数のAPI呼び出しがある場合、それらを論理的な順序で構成すること。
    - 取得した情報から最も適切と考えられる単一のスクリプトを作成すること。
    - 元のスクリプトが長い場合でも、編集指示に従って必要な変更を加えた後、元のスクリプトの残りの部分もすべて含めて完全なスクリプトを生成してください。

    ## 出力形式
    以下のマークダウン形式で回答してください。コードや説明以外の余計な文章は含めないでください。

    ## 生成されたスクリリプト
    ```python
    # ここにPythonスクリプトを記述（必ず最後まで完全に）
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



def execute_graph_qa(question: str, is_retry: bool = False):
    """
    GraphCypherQAChainを実行し、エラーハンドリングとリトライを行う。
    """
    try:
        return graph_qa.invoke({"query": question})
    except (ClientError, CypherSyntaxError) as e:
        print(f"\n--- [Error] Neo4jエラーが発生しました: {e} ---")
        
        if is_retry:
            print("--- [Error] 再試行も失敗しました。エラーをそのまま返します。 ---")
            raise e

        print("--- [Info] エラー情報を元にCypherクエリを再生成します... ---")
        new_question = f"""
        以下のCypherクエリを実行したところ、Neo4jデータベースでエラーが発生しました。
        エラーメッセージを参考に、正しいCypherクエリを再生成してください。

        【エラー内容】
        {str(e)}

        【元の質問】
        {question}
        """
        return execute_graph_qa(new_question, is_retry=True)
    except Exception as e:
        # Neo4j以外の予期せぬエラーもキャッチして表示
        print(f"\n--- [Error] 予期せぬエラーが発生しました: {e} ---")
        raise e

def ask(question: str, original_code: str = None, reference_code: str = None) -> str:
    """
    グラフ検索を使用して質問に回答します。
    original_codeは必須です。それを編集するタスクとして扱います。
    reference_codeが指定された場合は、それを参考スクリプトとしてプロンプトに含めます。
    """
    if not original_code:
        raise ValueError("original_codeは必須です。編集モードのみサポートされています。")

    if reference_code:
        final_question = f"""
        以下の【参考スクリプト】の構造やAPIの使用方法を参考にしながら、【元のスクリプト】を【編集指示】に従って修正してください。

        **重要: スクリプトは必ず最後まで完全に生成してください。元のスクリプトの全長を維持し、編集指示に関係する部分だけでなく、元のスクリプトのすべてのコードを含めてください。「続きます」「省略」「この後も...」などのコメントは一切追加しないでください。**

        【参考スクリプト】

        ```python
        {reference_code}
        ```

        【元のスクリプト】

        ```python
        {original_code}
        ```

        -----

        【編集指示】
        {question}

        【ブラケット追加の前提ルール】
        - ブラケットは Surfaces1/Surfaces2 の面ペアで定義し、BaseElement は profileXX[0] を基本とする。
        - 優先ペアは (板PLS×Profile FL) と (Profile FL×Profile FL)。板PLSは solidX または profileXX[1] を参照しうる。
        - AddAttachSurfaces と End1/End2 を持つスティフナ（ProfileType 1002/1003 等）をブラケット候補として探索し、各端部（End1/End2）に漏れなく配置する。
        - BracketType や Sf1EndElements/Sf2EndElements は参考スクリプト・既存サンプルの値を最優先で踏襲し、未知のフィールドを創作しない。
        """
    else:
        final_question = f"""
        以下の【元のスクリプト】を【編集指示】に従って修正してください。

        **重要: スクリプトは必ず最後まで完全に生成してください。編集指示に関係する部分だけでなく、元のスクリプトに追加したコードも含めてください。「続きます」「省略」「この後も...」などのコメントは一切追加しないでください。**

        【元のスクリプト】

        ```python
        {original_code}
        ```

        -----

        【編集指示】
        {question}

        【ブラケット追加の前提ルール】
        - ブラケットは Surfaces1/Surfaces2 の面ペアで定義し、BaseElement は profileXX[0] を基本とする。
        - 優先ペアは (板PLS×Profile FL) と (Profile FL×Profile FL)。板PLSは solidX または profileXX[1] を参照しうる。
        - AddAttachSurfaces と End1/End2 を持つスティフナ（ProfileType 1002/1003 等）をブラケット候補として探索し、各端部（End1/End2）に漏れなく配置する。
        - BracketType や Sf1EndElements/Sf2EndElements は参考スクリプト・既存サンプルの値を最優先で踏襲し、未知のフィールドを創作しない。
        """

    print("--- [Route: graph] Running Graph Search ---")
    result = execute_graph_qa(final_question)
    return result['result']

# \---------- CLI 入口 ----------

if __name__ == "__main__":
    import argparse
    import re

    # --- 引数パーサーの設定 ---
    parser = argparse.ArgumentParser(
        description="Generate or edit Python scripts for EvoShip based on user instructions.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=textwrap.dedent(__doc__)
    )
    parser.add_argument(
        "first_arg", 
        help="編集対象のファイルパス"
    )
    parser.add_argument(
        "instruction", 
        help="編集指示（引用符で囲む）"
    )
    parser.add_argument(
        "-o", "--output", 
        help="生成されたスクリプトの出力先ファイルパスを指定します。ディレクトリが存在しない場合は自動作成されます。"
    )
    parser.add_argument(
        "-r", "--reference",
        help="Path to a reference script file to use as a template or example."
    )
    
    args = parser.parse_args()

    original_code = None
    reference_code = None
    question = ""
    
    # --- 参考スクリプトの読み込み ---
    if args.reference:
        if not os.path.exists(args.reference):
            print(f"エラー: 参考スクリプトファイル '{args.reference}' が見つかりません。")
            sys.exit(1)
        try:
            with open(args.reference, 'r', encoding='utf-8') as f:
                reference_code = f.read()
            print(f"--- [Reference Script] Loading from: {args.reference} ---")
        except Exception as e:
            print(f"エラー: 参考スクリプトファイル '{args.reference}' の読み込み中にエラーが発生しました: {e}")
            sys.exit(1)
    
    # --- 引数の解析とモード判定 ---
    # 編集モードのみサポート
    if not os.path.exists(args.first_arg):
        print(f"エラー: ファイル '{args.first_arg}' が見つかりません。")
        parser.print_help()
        sys.exit(1)
    
    if not args.instruction:
        print("エラー: <ファイルパス>と<編集指示>の両方が必要です。")
        parser.print_help()
        sys.exit(1)
    
    file_path = args.first_arg
    question = args.instruction
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_code = f.read()
        print(f"--- [Mode: Edit] Loading script from: {file_path} ---")
    except Exception as e:
        print(f"エラー: ファイル '{file_path}' の読み込み中にエラーが発生しました: {e}")
        sys.exit(1)

    # --- 実行 ---
    try:
        answer = ask(question, original_code=original_code, reference_code=reference_code)
        
        # --- 出力処理とスクリプト抽出 ---
        if args.output:
            try:
                # 出力先パスの正規化と検証
                output_path = os.path.abspath(args.output)
                output_dir = os.path.dirname(output_path)
                
                # ディレクトリが指定されている場合、存在確認と作成
                if output_dir and not os.path.exists(output_dir):
                    try:
                        os.makedirs(output_dir, exist_ok=True)
                        print(f"--- Created output directory: {output_dir} ---")
                    except OSError as e:
                        print(f"エラー: 出力先ディレクトリ '{output_dir}' の作成に失敗しました: {e}")
                        sys.exit(1)
                
                # 既存ファイルの上書き確認
                if os.path.exists(output_path):
                    print(f"警告: ファイル '{output_path}' は既に存在します。上書きします。")
                
                # スクリプト部分を正規表現で抽出
                script_match = re.search(r"```python\n(.*?)```", answer, re.DOTALL)
                if script_match:
                    script_code = script_match.group(1).strip()
                    
                    # スクリプトをファイルに書き込む
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(script_code)
                    print(f"\n--- Script saved to: {output_path} ---")
                    
                    # 説明部分を抽出して表示
                    explanation_match = re.search(r"### スクリプトの説明\n\n(.*)", answer, re.DOTALL)
                    if explanation_match:
                        explanation = explanation_match.group(1).strip()
                        print("\n--- Script Explanation ---")
                        print(explanation)
                else:
                    print("\n--- Generated Answer (script not found) ---")
                    print(answer)
                    print(f"\n警告: スクリプトコードが見つからなかったため、ファイル '{output_path}' には保存されませんでした。")
                    
            except IOError as e:
                print(f"エラー: ファイル '{output_path}' の書き込みに失敗しました: {e}")
                sys.exit(1)
            except Exception as e:
                print(f"エラー: 出力処理中に予期せぬエラーが発生しました: {e}")
                sys.exit(1)
        else:
            # 出力ファイルが指定されていない場合は、従来通り全体を出力
            print("\n--- Generated Answer ---")
            print(answer)

    except ValueError as e:
        print(f"\nエラー: {e}")
    except Exception as e:
        print(f"\n予期せぬエラーが発生しました: {e}")
