"""
使い方:

[参考スクリプトの指定]
    python query0_norag.py ./script/sample_no_bracket.py "ブラケットをつけてください。" --reference ./script/samplename.py -o ./script/1225-1.py

"""
import sys
import os
import textwrap
import config
import re
import subprocess
from typing import Optional, Tuple

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from prompts.loader import (
    load_prompt, load_example, is_bracket_task,
    build_generation_prompt, build_analysis_prompt, build_bracket_section_prompt,
    build_bracket_section_prompt_with_error,
)

# ========== 定数定義 ==========
MAX_BRACKET_SEARCH_LINES = 200  # ブラケットパラメータ定義の探索範囲
CONTEXT_EXTRACTION_LINES = 50   # 関連変数抽出の探索範囲
DEFAULT_TIMEOUT_SEC = 600         # デフォルトのタイムアウト秒数
DEFAULT_MAX_RETRIES = 3          # デフォルトの最大再試行回数

# 正規表現パターンの定数化
BRACKET_PARAM_PATTERN = r'(bracketPram\w+|bracketParam\w+)'
PYTHON_CODE_BLOCK_PATTERN = r"```python\n(.*?)```"
BRACKET_DEFINITION_PATTERN = r'(bracketPram\w+\s*=\s*part\.CreateBracketParam\(\)[^\n]*\n(?:[^\n]*\n)*?bracket\w+\s*=\s*part\.CreateBracket\([^\n]+\))'

# ========== カスタム例外クラス ==========
class FileOperationError(Exception):
    """ファイル操作エラー"""
    pass

# ---------- LLM 生成 ----------
def create_llm(model_type: str = "gpt"):
    """CLI引数に基づいてLLMインスタンスを生成する。"""
    if model_type == "gpt":
        return ChatOpenAI(
            model="gpt-5.2",
            temperature=0,
            openai_api_key=config.OPENAI_API_KEY,
        )
    elif model_type == "gemini":
        if not config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set in .env. Required for --model gemini.")
        return ChatGoogleGenerativeAI(
            model="gemini-3-flash-preview",
            api_key=config.GEMINI_API_KEY,
            temperature=0,
        )
    else:
        raise ValueError(f"Unknown model type: '{model_type}'. Use 'gpt' or 'gemini'.")



def run_script(script_path: str, timeout_sec: int = DEFAULT_TIMEOUT_SEC) -> Tuple[bool, str, str, int]:
    """
    スクリプトを実行し、成功したかどうかと出力を返します。
    
    Args:
        script_path: 実行するスクリプトのパス
        timeout_sec: タイムアウト秒数（デフォルト: 600秒）
    
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


def ask(question: str, original_code: str, reference_code: Optional[str] = None, llm=None) -> str:
    """
    プロンプトのみを使用して質問に回答します。
    original_codeは必須です。それを編集するタスクとして扱います。
    reference_codeが指定された場合は、それを参考スクリプトとしてプロンプトに含めます。
    """
    if not original_code:
        raise ValueError("original_codeは必須です。編集モードのみサポートされています。")

    bracket = is_bracket_task(question, reference_code)

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
"""

    print("--- [Route: prompt-only] Running LLM Generation ---")

    # レイヤー分離されたプロンプトを組み立ててLLMを呼び出す
    prompt = build_generation_prompt(final_question, is_bracket=bracket)
    response = llm.invoke(prompt)

    return response.content


def fix_bracket_code(
    full_code: str,
    stderr: str,
    error_line_info: dict,
    bracket_context: dict,
    reference_code: Optional[str] = None,
    llm=None
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
        
        # 外部ファイルからブラケット修正テンプレートを読込
        template_text = load_prompt("bracket_fix")
        prompt = template_text.format(**prompt_vars)
        response = llm.invoke(prompt)
        
        # スクリプトコードを抽出
        script_match = re.search(PYTHON_CODE_BLOCK_PATTERN, response.content, re.DOTALL)
        if script_match:
            return script_match.group(1).strip()
        else:
            # コードブロックがない場合はそのまま返す（LLMが直接コードを返した場合）
            return response.content.strip()

# ---------- 3-Agent Pipeline ----------

BRACKET_SECTION_MARKER = "bracketPram1 = part.CreateBracketParam()"


def analyze_bracket_placement(
    instruction: str,
    original_code: str,
    reference_code: Optional[str] = None,
    llm=None,
) -> str:
    """Agent 1: ブラケット配置仕様ドキュメント（Markdown）を返す"""
    print("--- [Agent 1] Analyzing bracket placement ---")
    prompt = build_analysis_prompt(instruction, original_code, reference_code)
    response = llm.invoke(prompt)
    return response.content.strip()


def generate_bracket_section(
    analysis_document: str,
    reference_code: Optional[str] = None,
    llm=None,
) -> str:
    """Agent 2: ブラケットセクションのコードのみを返す"""
    print("--- [Agent 2] Generating bracket section ---")
    prompt = build_bracket_section_prompt(analysis_document, reference_code)
    response = llm.invoke(prompt)

    # ```python ブロックを抽出
    script_match = re.search(PYTHON_CODE_BLOCK_PATTERN, response.content, re.DOTALL)
    if script_match:
        return script_match.group(1).strip()
    return response.content.strip()


def generate_bracket_section_with_error(
    analysis_document: str,
    reference_code: Optional[str],
    error_context: dict,
    llm=None,
) -> str:
    """Agent 2 (リトライ): エラーコンテキスト付きでブラケットセクションを再生成する"""
    print("--- [Agent 2 Retry] Re-generating bracket section with error context ---")
    prompt = build_bracket_section_prompt_with_error(
        analysis_document, reference_code, error_context
    )
    response = llm.invoke(prompt)

    script_match = re.search(PYTHON_CODE_BLOCK_PATTERN, response.content, re.DOTALL)
    if script_match:
        return script_match.group(1).strip()
    return response.content.strip()


def merge_bracket_section(original_code: str, new_bracket_section: str) -> str:
    """
    元スクリプトの bracketPram1 行以降を new_bracket_section で置換する。
    マーカーが見つからなければ末尾に追記する。
    """
    idx = original_code.find(BRACKET_SECTION_MARKER)
    if idx != -1:
        # マーカー行の先頭を探して、その行ごと置換
        line_start = original_code.rfind('\n', 0, idx) + 1
        merged = original_code[:line_start] + new_bracket_section + "\n"
        print("--- [Merge] Replaced bracket section in original script ---")
    else:
        merged = original_code.rstrip() + "\n\n" + new_bracket_section + "\n"
        print("--- [Merge] Appended bracket section to original script ---")
    return merged


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
    no_exec: bool,
    llm=None,
    pipeline_mode: str = "three",
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
        print(f"--- Pipeline mode: {pipeline_mode} ---")

        current_code = None
        error_output = None
        # 3-agentモード用: 分析ドキュメントを保持（エラー修正ループで再利用）
        analysis_document = None

        for attempt in range(max_retries + 1):
            if attempt == 0:
                # 初回生成
                print(f"\n=== Attempt {attempt + 1}/{max_retries + 1}: Initial Generation ===")

                if pipeline_mode == "three":
                    # Agent 1: 分析ドキュメント生成
                    analysis_document = analyze_bracket_placement(
                        question, original_code, reference_code, llm=llm
                    )
                    # 分析ドキュメントの保存
                    if output_path:
                        analysis_path = output_path.replace('.py', '.analysis.md')
                        try:
                            with open(analysis_path, 'w', encoding='utf-8') as f:
                                f.write(analysis_document)
                            print(f"--- Analysis document saved to: {analysis_path} ---")
                        except IOError as e:
                            print(f"警告: 分析ドキュメントの保存に失敗しました: {e}")

                    # Agent 2: ブラケットセクション生成
                    bracket_section = generate_bracket_section(
                        analysis_document, reference_code, llm=llm
                    )
                    # プログラムマージ
                    script_code = merge_bracket_section(original_code, bracket_section)
                    answer = None

                elif pipeline_mode == "two":
                    # Agent 1: 分析ドキュメント生成
                    analysis_document = analyze_bracket_placement(
                        question, original_code, reference_code, llm=llm
                    )
                    if output_path:
                        analysis_path = output_path.replace('.py', '.analysis.md')
                        try:
                            with open(analysis_path, 'w', encoding='utf-8') as f:
                                f.write(analysis_document)
                            print(f"--- Analysis document saved to: {analysis_path} ---")
                        except IOError as e:
                            print(f"警告: 分析ドキュメントの保存に失敗しました: {e}")

                    # Agent 2: 完全スクリプト生成（従来のask相当、分析ドキュメントを指示として使用）
                    answer = ask(analysis_document, original_code=original_code, reference_code=reference_code, llm=llm)
                    script_code = None  # extract_script_codeで後処理

                else:
                    # off: 従来の1エージェント
                    answer = ask(question, original_code=original_code, reference_code=reference_code, llm=llm)
                    script_code = None

            else:
                # 修正ループ
                print(f"\n=== Attempt {attempt + 1}/{max_retries + 1}: Self-Correction ===")

                if not current_code or not error_output:
                    print("エラー: 修正に必要な情報が不足しています。")
                    break

                error_line_info = parse_traceback(error_output)
                bracket_context = extract_bracket_failure_context(current_code, error_line_info)

                if pipeline_mode == "three" and analysis_document:
                    # 3-agentエラー修正: Agent 2 をエラーコンテキスト付きで再実行 → 元コードにマージ
                    error_ctx = {
                        "stderr": error_output,
                        "line_number": error_line_info.get("line_number", "unknown"),
                        "error_line": bracket_context.get("error_line", ""),
                        "bracket_param_section": bracket_context.get("bracket_param_definition", ""),
                    }
                    fixed_bracket_section = generate_bracket_section_with_error(
                        analysis_document, reference_code, error_ctx, llm=llm
                    )
                    # original_code にマージ（current_code ではなく）して前回の失敗コード蓄積を防ぐ
                    script_code = merge_bracket_section(original_code, fixed_bracket_section)
                    current_code = script_code
                    answer = None
                else:
                    current_code = fix_bracket_code(
                        current_code,
                        error_output,
                        error_line_info,
                        bracket_context,
                        reference_code,
                        llm=llm
                    )
                    answer = None
                    script_code = current_code

            # スクリプト抽出と保存
            if output_path:
                try:
                    if attempt == 0:
                        if pipeline_mode == "three":
                            # script_codeはすでにマージ済み
                            if not script_code:
                                print("警告: ブラケットセクションのマージに失敗しました。")
                                break
                        elif script_code is None:
                            # two / off モード: answerからコードを抽出
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

                        save_script_file(output_path, script_code, attempt, keep_attempts)

                        if keep_attempts and attempt > 0 and error_output:
                            save_error_log(output_path, error_output, attempt)

                        if attempt == 0 and pipeline_mode != "three":
                            explanation = extract_explanation(answer) if answer else None
                            if explanation:
                                print("\n--- Script Explanation ---")
                                print(explanation)

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
                            print("\n--- Script saved (execution skipped by --no-exec) ---")
                            break
                except FileOperationError as e:
                    print(f"エラー: {e}")
                    sys.exit(1)
                except Exception as e:
                    print(f"エラー: 出力処理中に予期せぬエラーが発生しました: {e}")
                    sys.exit(1)
            else:
                if attempt == 0:
                    if pipeline_mode == "three":
                        print("\n--- Generated Bracket Section (merged) ---")
                        print(script_code[:2000] if script_code else "(empty)")
                    else:
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
    parser.add_argument(
        "--model",
        choices=["gpt", "gemini"],
        default="gpt",
        help="使用するLLMモデル（デフォルト: gpt）。'gpt' = GPT-5.1, 'gemini' = Gemini 3 Pro Preview"
    )
    parser.add_argument(
        "--pipeline-mode",
        choices=["off", "two", "three"],
        default="three",
        help=(
            "パイプラインモード（デフォルト: three）。\n"
            "  three: Agent1(分析) → Agent2(ブラケットセクション) → プログラムマージ（高速）\n"
            "  two:   Agent1(分析) → Agent2(完全スクリプト生成)\n"
            "  off:   従来の1エージェント"
        )
    )
    
    args = parser.parse_args()

    # LLMインスタンスの生成
    llm = create_llm(args.model)
    print(f"--- Using model: {args.model} ---")

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
            no_exec=args.no_exec,
            llm=llm,
            pipeline_mode=args.pipeline_mode,
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

