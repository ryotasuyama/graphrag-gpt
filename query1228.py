"""
使い方:

[参考スクリプトの指定]
    python query1227.py ./script/sample_no_bracket.py "ブラケットをつけてください。" --reference ./script/samplename.py -o ./script/1225-1.py

"""
import sys
import os
import textwrap
import config
import re
import subprocess
from typing import Optional, Tuple

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

from langchain_neo4j import Neo4jGraph, GraphCypherQAChain
from langchain_core.prompts import PromptTemplate
from neo4j.exceptions import ClientError, CypherSyntaxError

# ========== 定数定義 ==========
MAX_BRACKET_SEARCH_LINES = 200  # ブラケットパラメータ定義の探索範囲
CONTEXT_EXTRACTION_LINES = 100  # コンテキスト抽出の範囲
GRAPH_SEARCH_TOP_K = 10000      # グラフ検索の最大結果数
DEFAULT_TIMEOUT_SEC = 60         # デフォルトのタイムアウト秒数
DEFAULT_MAX_RETRIES = 3          # デフォルトの最大再試行回数

# 正規表現パターンの定数化
BRACKET_PARAM_PATTERN = r'(bracketPram\w+|bracketParam\w+)'
PYTHON_CODE_BLOCK_PATTERN = r"```python\n(.*?)```"
BRACKET_DEFINITION_PATTERN = r'(bracketPram\w+\s*=\s*part\.CreateBracketParam\(\)[^\n]*\n(?:[^\n]*\n)*?bracket\w+\s*=\s*part\.CreateBracket\([^\n]+\))'

# ========== プロンプト用共通ルール定数 ==========
SCRIPT_COMPLETION_REQUIREMENT = """
**重要: スクリプトは必ず最後まで完全に生成してください。**
- 元のスクリプトの全長を維持し、すべてのコードを含めてください。
- 「続きます」「省略」「この後も...」などのコメントは一切追加しないでください。
"""

BRACKET_DOMAIN_RULES = """
## ブラケット生成の基本ルール
- ブラケットは Surfaces1/Surfaces2 の面ペアで定義し、BaseElement は profileXX[0] を基本とする。
- 優先ペアは (板PLS×Profile FL) と (Profile FL×Profile FL)。板PLSは solidX または profileXX[1] を参照しうる。
- AddAttachSurfaces と End1/End2 を持つスティフナ（ProfileType 1002/1003 等）をブラケット候補として探索し、各端部（End1/End2）に漏れなく配置する。
- BracketType や Sf1EndElements/Sf2EndElements は参考スクリプト・既存サンプルの値を最優先で踏襲し、未知のフィールドを創作しない。
- `part.CreateBracket(bracketParam, <flag>)` の第2引数は必ず False にする（True は作成時に非表示になるため禁止）。
- ブラケット作成後に `part.BlankElement(bracketX, True)` を入れない。
"""

BRACKET_COVERAGE_RULES = """
## ブラケット網羅性の要件
- Deck.DP が生成される箇所では、同一FR/DLに対して AP/BP/CP/DP を系列展開して網羅すること。
- DL00 の Deck.A/B/C/D も生成対象とする。
- 同名ブラケットが複数必要な場合は同数を再現すること。
- 左右対称が成立する場合は対称側も生成すること（MirrorCopy可）。
"""

BRACKET_REFERENCE_ANALYSIS_GUIDE = """
## 参考スクリプトの分析・適用指針
参考スクリプトが提供されている場合、以下の3点を徹底的に分析し、修正後のスクリプトに反映してください：
1. **接続対象（Target Members）の特定:**
   - ブラケットがどの部材に対して取り付けられているか、その組み合わせを抽出。
   - 取り付け位置（StartPoint, EndPoint, Intersectionなど）の計算ロジックを正確に読み取る。
   - ブラケットは Surfaces1 / Surfaces2 の "面ペア" で定義される点に注意。
2. **パラメータの依存関係（Parameter Logic）:**
   - ブラケットのサイズ（Height, Width, Thickness）が、接続先の部材サイズや属性からどのように算出されているかを確認。
   - ブラケットの種類（Type）や向き（Orientation/Vector）を決定するパラメータの組み合わせパターンを模倣。
   - 参考スクリプトに BracketType（例: 1501/1505）や Sf1EndElements/Sf2EndElements がある場合は必ず踏襲。
3. **配置の完全性とエラー回避:**
   - 複数の箇所にブラケットが必要な場合、ループ処理や条件分岐がどのように行われているかを確認し、「漏れなく」配置。
   - API呼び出しの前に必要な初期化処理や、戻り値の型チェックが参考スクリプトで行われている場合、それを必ず継承。
"""

# ========== カスタム例外クラス ==========
class ScriptExecutionError(Exception):
    """スクリプト実行エラー"""
    pass

class ScriptGenerationError(Exception):
    """スクリプト生成エラー"""
    pass

class FileOperationError(Exception):
    """ファイル操作エラー"""
    pass

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

question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

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
    ユーザーの質問を解釈し、提供されたグラフスキーマ情報に基づいて、その答えを見つけるための最適なCypherクエリを生成してください。

    ## グラフスキーマ情報
    {schema}

    ## クエリ生成の指示
    1.  **思考プロセスに従う:**
        - **Step 1. 意図の理解:** ユーザーが何をしたいのか特定する。
        - **Step 2. スキーマとのマッピング:** 検索の起点となるノードとリレーションを選択する。
        - **Step 3. 構文の安全性の確保:** **重要：collect() 内でさらに collect() を使用するような、集計関数のネストは絶対に避けてください。** 複雑な構造が必要な場合は、WITH 句を使ってデータをフラットに処理してから次のステップに進んでください。

    2.  **検索戦略のヒント:**
        - APIの引数や属性を取得したい場合は、結果を RETURN する際に複雑な MAP 構造を作りすぎないようにしてください。
        - キーワード検索には toLower() と CONTAINS を活用してください。

    ## 出力要件
    - **【最重要】「collect(DISTINCT {{ ..., attrs: collect(...) }})」のような、集計関数の入れ子は禁止です。**
    - 生成されたCypherクエリのみを、コードブロックなしで文字列として出力してください。
    - 説明、前置き、謝罪は一切含めないでください。
    - クエリは必ず MATCH や RETURN などのキーワードから開始してください。
    ---
    **質問:** {question}
    **Cypherクエリ:**
    """

CYPHER_GENERATION_PROMPT = PromptTemplate(
    input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE_JP
)

QA_TEMPLATE = (
    """
あなたは、CADアプリケーション「EvoShip」をPythonで操作するエキスパートです。
ユーザーの要求とナレッジグラフから取得した情報を基に、実行可能なPythonスクリプトを生成してください。

ユーザーの要求:
{question}

ナレッジグラフから取得した関連情報:
{context}

"""
    + BRACKET_REFERENCE_ANALYSIS_GUIDE
    + BRACKET_DOMAIN_RULES
    + SCRIPT_COMPLETION_REQUIREMENT
    + """
## スクリプト生成の要件
- **元のスクリプトを基に編集・修正を行ってください。**
- **「参考スクリプト」が提供されている場合は、その構造、APIの使用方法、コーディングスタイルを参考にしながらスクリプトを編集してください。**
- **【禁止事項】以下のようなコメントや説明をコード内に追加しないでください：**
  - 「この後も続きます」「省略」「...」「この後も元スクリプトと同様に...」などの途中終了を示すコメント
  - 「上記3箇所の...」のような部分的な説明コメント
  - 「実運用では...」「注意: 実運用では...」のような注意書きコメント
- メソッドの返り値は、後続のメソッドで利用するために変数に格納すること。
- 複数のAPI呼び出しがある場合、それらを論理的な順序で構成すること。
- 取得した情報から最も適切と考えられる単一のスクリプトを作成すること。

## 出力形式
以下のマークダウン形式で回答してください。コードや説明以外の余計な文章は含めないでください。

## 生成されたスクリプト
```python
# ここにPythonスクリプトを記述（必ず最後まで完全に）
```

### スクリプトの説明
生成したスクリプトの説明を簡潔に記述してください。
"""
)

QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"], template=QA_TEMPLATE
)

# ---------- ブラケットパラメータ特化の修正プロンプト ----------
BRACKET_FIX_TEMPLATE = (
    """
あなたは、CADアプリケーション「EvoShip」のブラケット生成コードを修正するエキスパートです。
以下のPythonスクリプトを実行したところ、CreateBracket呼び出しでCOM例外が発生しました。
エラー情報を分析し、**最小限の変更で**ブラケットパラメータを修正した完全なPythonスクリプトを生成してください。

## 重要：最小変更ポリシー（必ず守る）
- **変更対象は「エラー行の CreateBracket に渡している bracketParam の定義と、それに直結する補助変数」だけです。**
- それ以外のコード（生成された形状、部材生成順序、他のブラケット）は **原則そのまま**にしてください。
- どうしても周辺の参照（faces の取り方等）を直す必要がある場合でも、変更は **エラー行の前後ブロック内に限定**してください。
- 出力は **完成した全スクリプト**（省略なし、` ```python ... ``` ` で囲む）のみです。

## エラー情報（Traceback）
{error_traceback}

## 失敗行とその周辺コンテキスト
失敗行（行{error_line_number}）:
```python
{error_line}
```

前後のコンテキスト（前{context_lines}行）:
```python
{context_before}
{error_line}
{context_after}
```

## 対象ブラケットパラメータの定義
{bracket_param_section}

## ブラケット修正のチェックポイント
以下の観点を順に確認し、問題があれば修正してください：
1. **表示状態（Blank）**: `CreateBracket`の第2引数は必ずFalse、`BlankElement(..., True)`は削除
2. **Surfaces1/Surfaces2**: 参照面がNone/未生成でないか、面ペア順序が参考スクリプトと整合するか
3. **BaseElement**: 原則`profileXX[0]`を使用、solidを渡していないか
4. **EndElements**: `AddEnd1Elements/AddEnd2Elements`に対応する要素が欠けていないか
5. **BracketType/フィールド**: 参考スクリプトの値を踏襲し、勝手に増減しない
6. **寸法**: Height/Width/Thicknessが0以下でないか、適切な範囲内か
7. **向き（Orientation/Vector）**: 参照面の法線に対して不正でないか

"""
    + BRACKET_DOMAIN_RULES
    + """
## 参考スクリプト（該当する CreateBracket 例）
{reference_snippet}

## 元のスクリプト全体
```python
{full_code}
```

## 出力形式
修正後の完全なPythonスクリプトのみを以下の形式で出力してください。説明やコメントは不要です。

```python
# 修正後の完全なスクリプト（省略なし）
```
"""
)

BRACKET_FIX_PROMPT = PromptTemplate(
    input_variables=[
        "error_traceback",
        "error_line_number",
        "error_line",
        "context_before",
        "context_after",
        "context_lines",
        "bracket_param_section",
        "reference_snippet",
        "full_code"
    ],
    template=BRACKET_FIX_TEMPLATE
)

graph_qa = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    verbose=True,
    cypher_prompt=CYPHER_GENERATION_PROMPT,
    qa_prompt=QA_PROMPT,
    allow_dangerous_requests=True,
    top_k=GRAPH_SEARCH_TOP_K,
)



def run_script(script_path: str, timeout_sec: int = DEFAULT_TIMEOUT_SEC) -> Tuple[bool, str, str, int]:
    """
    スクリプトを実行し、成功したかどうかと出力を返します。
    
    Args:
        script_path: 実行するスクリプトのパス
        timeout_sec: タイムアウト秒数（デフォルト: 60秒）
    
    Returns:
        (success: bool, stdout: str, stderr: str, returncode: int)
    """
    print(f"--- Executing script: {script_path} ---")
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=timeout_sec
        )
        
        if result.returncode == 0:
            return True, result.stdout, result.stderr, result.returncode
        else:
            return False, result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        error_msg = f"Script execution timed out after {timeout_sec} seconds."
        return False, "", error_msg, -1
    except FileNotFoundError:
        error_msg = f"Python interpreter not found: {sys.executable}"
        return False, "", error_msg, -1
    except Exception as e:
        error_msg = f"Error executing script: {str(e)}"
        return False, "", error_msg, -1


def parse_traceback(stderr: str) -> dict:
    """
    Tracebackから失敗情報を抽出します。
    
    Returns:
        {
            'file_path': str or None,
            'line_number': int or None,
            'line_code': str or None,
            'exception_type': str or None,
            'exception_message': str or None,
            'full_traceback': str
        }
    """
    result = {
        'file_path': None,
        'line_number': None,
        'line_code': None,
        'exception_type': None,
        'exception_message': None,
        'full_traceback': stderr
    }
    
    if not stderr:
        return result
    
    # 行番号の抽出（例: "line 905" または "File \"...\", line 905"）
    line_match = re.search(r'line\s+(\d+)', stderr)
    if line_match:
        result['line_number'] = int(line_match.group(1))
    
    # ファイルパスの抽出
    file_match = re.search(r'File\s+["\']([^"\']+)["\']', stderr)
    if file_match:
        result['file_path'] = file_match.group(1)
    
    # 例外タイプの抽出（例: "pywintypes.com_error", "AttributeError"）
    exception_match = re.search(r'(\w+(?:\.\w+)*Error|Exception|Error):\s*(.*?)(?:\n|$)', stderr, re.MULTILINE)
    if exception_match:
        result['exception_type'] = exception_match.group(1)
        result['exception_message'] = exception_match.group(2).strip()
    
    return result


def extract_bracket_failure_context(full_code: str, error_line_info: dict, context_lines: int = 50) -> dict:
    """
    失敗行周辺のブラケットパラメータ定義を抽出します。
    
    Args:
        full_code: スクリプト全体のコード
        error_line_info: parse_traceback()の結果
        context_lines: 前後何行を取得するか（デフォルト: 50）
    
    Returns:
        {
            'error_line': str,
            'context_before': str,
            'context_after': str,
            'bracket_param_name': str or None,
            'bracket_param_definition': str or None,
            'related_variables': list[str]
        }
    """
    result = {
        'error_line': '',
        'context_before': '',
        'context_after': '',
        'bracket_param_name': None,
        'bracket_param_definition': None,
        'related_variables': []
    }
    
    if not full_code or not error_line_info.get('line_number'):
        return result
    
    lines = full_code.split('\n')
    line_num = error_line_info['line_number']
    
    # 行番号は1ベース、配列は0ベースなので調整
    idx = line_num - 1
    if idx < 0 or idx >= len(lines):
        return result
    
    # 失敗行のコード
    result['error_line'] = lines[idx]
    
    # 前後のコンテキスト
    start_idx = max(0, idx - context_lines)
    end_idx = min(len(lines), idx + context_lines + 1)
    result['context_before'] = '\n'.join(lines[start_idx:idx])
    result['context_after'] = '\n'.join(lines[idx+1:end_idx])
    
    # bracketParam変数名の抽出（例: bracketPramC1, bracketParam1）
    bracket_param_match = re.search(BRACKET_PARAM_PATTERN, result['error_line'])
    if bracket_param_match:
        result['bracket_param_name'] = bracket_param_match.group(1)
        
        # 該当パラメータの定義ブロックを探す
        param_name = result['bracket_param_name']
        # 定義パターン: bracketPramX = part.CreateBracketParam()
        definition_pattern = rf'{re.escape(param_name)}\s*=\s*part\.CreateBracketParam\(\)'
        
        # 定義行を探す（失敗行より前を探索）
        for i in range(idx - 1, max(0, idx - MAX_BRACKET_SEARCH_LINES), -1):
            if re.search(definition_pattern, lines[i]):
                # 定義が見つかったら、そこから失敗行までのブロックを抽出
                definition_start = i
                definition_end = idx
                result['bracket_param_definition'] = '\n'.join(lines[definition_start:definition_end])
                break
        
        # 関連変数（profileXX, solidX, faces等）を抽出
        context_block = '\n'.join(lines[max(0, idx - CONTEXT_EXTRACTION_LINES):idx])
        var_patterns = [
            r'profile\d+',
            r'solid\d+',
            r'faces\d*',
            r'Surfaces\d+',
            r'BaseElement',
        ]
        for pattern in var_patterns:
            matches = re.findall(pattern, context_block, re.IGNORECASE)
            result['related_variables'].extend(matches)
        
        result['related_variables'] = list(set(result['related_variables']))
    
    return result


def execute_graph_qa(question: str, is_retry: bool = False) -> dict:
    """
    GraphCypherQAChainを実行し、エラーハンドリングとリトライを行う。
    
    Args:
        question: 質問文字列
        is_retry: 再試行フラグ
    
    Returns:
        GraphCypherQAChainの実行結果（辞書）
    
    Raises:
        ClientError: Neo4jクライアントエラー
        CypherSyntaxError: Cypher構文エラー
        Exception: その他の予期せぬエラー
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

def ask(question: str, original_code: str, reference_code: Optional[str] = None) -> str:
    """
    グラフ検索を使用して質問に回答します。
    original_codeは必須です。それを編集するタスクとして扱います。
    reference_codeが指定された場合は、それを参考スクリプトとしてプロンプトに含めます。
    """
    if not original_code:
        raise ValueError("original_codeは必須です。編集モードのみサポートされています。")

    # ブラケット関連タスクの場合、questionに網羅要件を自動追記
    if "ブラケット" in question:
        question = question + BRACKET_COVERAGE_RULES

    if reference_code:
        final_question = f"""
以下の【参考スクリプト】の構造やAPIの使用方法を参考にしながら、【元のスクリプト】を【編集指示】に従って修正してください。

{SCRIPT_COMPLETION_REQUIREMENT}

【参考スクリプト】

```python
{reference_code}
```

【元のスクリプト】

```python
{original_code}
```

【編集指示】
{question}

{BRACKET_DOMAIN_RULES}
{BRACKET_COVERAGE_RULES if "ブラケット" in question else ""}
"""
    else:
        final_question = f"""
以下の【元のスクリプト】を【編集指示】に従って修正してください。

{SCRIPT_COMPLETION_REQUIREMENT}

【元のスクリプト】

```python
{original_code}
```

【編集指示】
{question}

{BRACKET_DOMAIN_RULES}
{BRACKET_COVERAGE_RULES if "ブラケット" in question else ""}
"""

    print("--- [Route: graph] Running Graph Search ---")
    result = execute_graph_qa(final_question)
    return result['result']


def fix_bracket_code(
    full_code: str,
    stderr: str,
    error_line_info: dict,
    bracket_context: dict,
    reference_code: Optional[str] = None
    ) -> str:
        """
        ブラケットパラメータ特化の修正をLLMに依頼します。
        
        Args:
            full_code: スクリプト全体のコード
            stderr: エラー出力
            error_line_info: parse_traceback()の結果
            bracket_context: extract_bracket_failure_context()の結果
            reference_code: 参考スクリプト（オプション）
        
        Returns:
            修正後のスクリプトコード
        """
        print("--- Requesting bracket-specific fix from LLM ---")
        
        # 参考スクリプトから該当するCreateBracket例を抽出（簡易版）
        reference_snippet = ""
        if reference_code:
            # bracketParam定義とCreateBracket呼び出しのブロックを抽出
            matches = re.findall(BRACKET_DEFINITION_PATTERN, reference_code, re.MULTILINE)
            if matches:
                # 最初の2-3個の例を参考として使用
                reference_snippet = '\n\n'.join(matches[:3])
        
        if not reference_snippet:
            reference_snippet = "# 参考スクリプトが提供されていないか、該当例が見つかりませんでした。"
        
        # bracket_param_sectionの準備
        bracket_param_section = bracket_context.get('bracket_param_definition', '')
        if not bracket_param_section:
            bracket_param_section = f"# ブラケットパラメータ '{bracket_context.get('bracket_param_name', 'unknown')}' の定義が見つかりませんでした。\n# エラー行: {bracket_context.get('error_line', '')}"
        
        # プロンプトの準備
        prompt_vars = {
            "error_traceback": stderr,
            "error_line_number": error_line_info.get('line_number', 'unknown'),
            "error_line": bracket_context.get('error_line', ''),
            "context_before": bracket_context.get('context_before', ''),
            "context_after": bracket_context.get('context_after', ''),
            "context_lines": 50,
            "bracket_param_section": bracket_param_section,
            "reference_snippet": reference_snippet,
            "full_code": full_code
        }
        
        prompt = BRACKET_FIX_PROMPT.format(**prompt_vars)
        response = llm.invoke(prompt)
        
        # スクリプトコードを抽出
        script_match = re.search(PYTHON_CODE_BLOCK_PATTERN, response.content, re.DOTALL)
        if script_match:
            return script_match.group(1).strip()
        else:
            # コードブロックがない場合はそのまま返す（LLMが直接コードを返した場合）
            return response.content.strip()

# ---------- CLI 入口 ----------

def load_script_files(file_path: str, reference_path: Optional[str] = None) -> Tuple[str, Optional[str]]:
    """
    スクリプトファイルを読み込む
    
    Args:
        file_path: 編集対象のファイルパス
        reference_path: 参考スクリプトのファイルパス（オプション）
    
    Returns:
        (original_code, reference_code)
    
    Raises:
        FileOperationError: ファイル読み込みに失敗した場合
    """
    if not os.path.exists(file_path):
        raise FileOperationError(f"ファイル '{file_path}' が見つかりません。")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_code = f.read()
        print(f"--- [Mode: Edit] Loading script from: {file_path} ---")
    except Exception as e:
        raise FileOperationError(f"ファイル '{file_path}' の読み込み中にエラーが発生しました: {e}")
    
    reference_code = None
    if reference_path:
        if not os.path.exists(reference_path):
            raise FileOperationError(f"参考スクリプトファイル '{reference_path}' が見つかりません。")
        try:
            with open(reference_path, 'r', encoding='utf-8') as f:
                reference_code = f.read()
            print(f"--- [Reference Script] Loading from: {reference_path} ---")
        except Exception as e:
            raise FileOperationError(f"参考スクリプトファイル '{reference_path}' の読み込み中にエラーが発生しました: {e}")
    
    return original_code, reference_code


def prepare_output_directory(output_path: str) -> None:
    """
    出力先ディレクトリを作成する
    
    Args:
        output_path: 出力先ファイルパス
    
    Raises:
        FileOperationError: ディレクトリ作成に失敗した場合
    """
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir, exist_ok=True)
            print(f"--- Created output directory: {output_dir} ---")
        except OSError as e:
            raise FileOperationError(f"出力先ディレクトリ '{output_dir}' の作成に失敗しました: {e}")


def extract_script_code(answer: str) -> Optional[str]:
    """
    LLMの回答からPythonスクリプトコードを抽出する
    
    Args:
        answer: LLMの回答文字列
    
    Returns:
        抽出されたスクリプトコード、見つからない場合はNone
    """
    script_match = re.search(PYTHON_CODE_BLOCK_PATTERN, answer, re.DOTALL)
    if script_match:
        return script_match.group(1).strip()
    return None


def extract_explanation(answer: str) -> Optional[str]:
    """
    LLMの回答からスクリプトの説明を抽出する
    
    Args:
        answer: LLMの回答文字列
    
    Returns:
        抽出された説明、見つからない場合はNone
    """
    explanation_match = re.search(r"### スクリプトの説明\n\n(.*)", answer, re.DOTALL)
    if explanation_match:
        return explanation_match.group(1).strip()
    return None


def save_script_file(file_path: str, script_code: str, attempt: Optional[int] = None, keep_attempts: bool = True) -> None:
    """
    スクリプトをファイルに保存する
    
    Args:
        file_path: 保存先ファイルパス
        script_code: 保存するスクリプトコード
        attempt: 試行回数（指定された場合、attempt番号付きファイルも作成）
        keep_attempts: attempt番号付きファイルを作成するかどうか
    
    Raises:
        FileOperationError: ファイル書き込みに失敗した場合
    """
    try:
        # attempt番号付きファイルの保存
        if keep_attempts and attempt is not None and attempt > 0:
            attempt_path = file_path.replace('.py', f'.attempt{attempt}.py')
            with open(attempt_path, 'w', encoding='utf-8') as f:
                f.write(script_code)
            print(f"--- Script saved to: {attempt_path} ---")
        
        # 最新版の保存
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(script_code)
        print(f"--- Script saved to: {file_path} ---")
    except IOError as e:
        raise FileOperationError(f"ファイル '{file_path}' の書き込みに失敗しました: {e}")


def save_error_log(file_path: str, error_output: str, attempt: Optional[int] = None) -> None:
    """
    エラーログをファイルに保存する
    
    Args:
        file_path: 元のファイルパス
        error_output: エラー出力文字列
        attempt: 試行回数（Noneの場合はfinalログとして保存）
    """
    if not error_output:
        return
    
    try:
        if attempt is not None:
            error_log_path = file_path.replace('.py', f'.attempt{attempt}.stderr.log')
        else:
            error_log_path = file_path.replace('.py', '.final.stderr.log')
        
        with open(error_log_path, 'w', encoding='utf-8') as f:
            f.write(error_output)
        print(f"--- Error log saved to: {error_log_path} ---")
    except IOError as e:
        print(f"警告: エラーログの保存に失敗しました: {e}")


def process_generation_loop(
    question: str,
    original_code: str,
    reference_code: Optional[str],
    output_path: Optional[str],
    max_retries: int,
    timeout_sec: int,
    keep_attempts: bool,
    no_exec: bool
    ) -> None:
        """
        スクリプト生成と実行のメインループ
        
        Args:
            question: 編集指示
            original_code: 元のスクリプトコード
            reference_code: 参考スクリプトコード（オプション）
            output_path: 出力先ファイルパス（Noneの場合は標準出力）
            max_retries: 最大再試行回数
            timeout_sec: タイムアウト秒数
            keep_attempts: 各試行のスクリプトを保存するかどうか
            no_exec: 実行をスキップするかどうか
        """
        current_code = None
        error_output = None
        
        for attempt in range(max_retries + 1):
            if attempt == 0:
                # 初回生成
                print(f"\n=== Attempt {attempt + 1}/{max_retries + 1}: Initial Generation ===")
                answer = ask(question, original_code=original_code, reference_code=reference_code)
            else:
                # 修正ループ
                print(f"\n=== Attempt {attempt + 1}/{max_retries + 1}: Self-Correction ===")
                
                if not current_code or not error_output:
                    print("エラー: 修正に必要な情報が不足しています。")
                    break
                
                # エラー情報を解析
                error_line_info = parse_traceback(error_output)
                bracket_context = extract_bracket_failure_context(current_code, error_line_info)
                
                # 修正を依頼
                current_code = fix_bracket_code(
                    current_code,
                    error_output,
                    error_line_info,
                    bracket_context,
                    reference_code
                )
                answer = None
            
            # スクリプト抽出と保存
            if output_path:
                try:
                    if attempt == 0:
                        script_code = extract_script_code(answer)
                        if not script_code:
                            print("\n--- Generated Answer (script not found) ---")
                            print(answer)
                            print(f"\n警告: スクリプトコードが見つからなかったため、ファイル '{output_path}' には保存されませんでした。")
                            break
                    else:
                        script_code = current_code
                    
                    if script_code:
                        current_code = script_code
                        
                        # ファイル保存
                        save_script_file(output_path, script_code, attempt, keep_attempts)
                        
                        # エラーログの保存（修正ループの場合）
                        if keep_attempts and attempt > 0 and error_output:
                            save_error_log(output_path, error_output, attempt)
                        
                        # 初回のみ説明を表示
                        if attempt == 0:
                            explanation = extract_explanation(answer)
                            if explanation:
                                print("\n--- Script Explanation ---")
                                print(explanation)
                        
                        # 実行（--no-execが指定されていない場合）
                        if not no_exec:
                            success, stdout, stderr, returncode = run_script(output_path, timeout_sec)
                            
                            if success:
                                print("\n--- Execution Successful ---")
                                if stdout:
                                    print(stdout)
                                break
                            else:
                                print(f"\n--- Execution Failed (Attempt {attempt + 1}) ---")
                                if stderr:
                                    print(stderr)
                                error_output = stderr
                                
                                if attempt == max_retries:
                                    print("\n--- Max retries reached. Final script saved. ---")
                                    if keep_attempts and error_output:
                                        save_error_log(output_path, error_output)
                        else:
                            # --no-execが指定されている場合は実行せず終了
                            print("\n--- Script saved (execution skipped by --no-exec) ---")
                            break
                except FileOperationError as e:
                    print(f"エラー: {e}")
                    sys.exit(1)
                except Exception as e:
                    print(f"エラー: 出力処理中に予期せぬエラーが発生しました: {e}")
                    sys.exit(1)
            else:
                # 出力ファイルが指定されていない場合は、従来通り全体を出力
                if attempt == 0:
                    print("\n--- Generated Answer ---")
                    print(answer)
                break


if __name__ == "__main__":
    import argparse

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
    parser.add_argument(
        "--max-retries",
        type=int,
        default=DEFAULT_MAX_RETRIES,
        help=f"最大再試行回数（デフォルト: {DEFAULT_MAX_RETRIES}）"
    )
    parser.add_argument(
        "--timeout-sec",
        type=int,
        default=DEFAULT_TIMEOUT_SEC,
        help=f"スクリプト実行のタイムアウト秒数（デフォルト: {DEFAULT_TIMEOUT_SEC}）"
    )
    parser.add_argument(
        "--keep-attempts",
        action="store_true",
        default=True,
        help="各試行のスクリプトを保存する（デフォルト: ON）"
    )
    parser.add_argument(
        "--no-keep-attempts",
        dest="keep_attempts",
        action="store_false",
        help="各試行のスクリプトを保存しない"
    )
    parser.add_argument(
        "--no-exec",
        action="store_true",
        default=False,
        help="スクリプトを実行せず、保存のみ行う（デフォルト: OFF）"
    )
    
    args = parser.parse_args()
    
    # 引数の検証
    if not args.instruction:
        print("エラー: <ファイルパス>と<編集指示>の両方が必要です。")
        parser.print_help()
        sys.exit(1)
    
    try:
        # ファイル読み込み
        original_code, reference_code = load_script_files(args.first_arg, args.reference)
        
        # 出力先ディレクトリの準備
        output_path = None
        if args.output:
            output_path = os.path.abspath(args.output)
            prepare_output_directory(output_path)
        
        # メイン処理
        process_generation_loop(
            question=args.instruction,
            original_code=original_code,
            reference_code=reference_code,
            output_path=output_path,
            max_retries=args.max_retries,
            timeout_sec=args.timeout_sec,
            keep_attempts=args.keep_attempts,
            no_exec=args.no_exec
        )
    
    except FileOperationError as e:
        print(f"\nエラー: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"\nエラー: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n予期せぬエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
