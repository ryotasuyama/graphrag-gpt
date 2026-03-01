from __future__ import annotations
import os, json, re, hashlib, datetime, sys, subprocess, locale
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import shutil
import glob
import hashlib  # _sha12_from_file で使用


# --- 出力の文字化け対策（Windows cp932 向け） ---
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# ==== ここから：元ファイルの “設定値” は維持 ====
def sha1(text: str) -> str:
    import hashlib
    return hashlib.sha1(text.encode("utf-8", errors="ignore")).hexdigest()[:12]

load_dotenv("API.env")

# --- GUI側で上書きされる想定のダミー取得関数 ---
def get_input_py_path() -> Optional[str]:
    return None

def get_instruction_text() -> str:
    return ""

def get_history() -> List[Dict[str, str]]:
    """形式: [{"role":"user","content":"..."},{"role":"assistant","content":"..."}]"""
    return []

def get_log_dir() -> str:
    return "chatlogs"

def get_use_previous_base() -> bool:
    """
    直近の out.py を基底にするかをGUIから注入。
    デフォルト False（= ドロップが無ければ新規作成）。
    """
    return False

# ==== 追加：曖昧表現の調整（前処理） ====
_ZEN2HAN_TABLE = str.maketrans({
    "０":"0","１":"1","２":"2","３":"3","４":"4",
    "５":"5","６":"6","７":"7","８":"8","９":"9",
    "（":"(","）":")","［":"[","］":"]","｛":"{","｝":"}",
    "：":":","；":";","、":",","。":".","　":" "
})


def normalize_instruction(text: str) -> str:
    """
    - 全角→半角（数字・記号）/ 連続空白畳み
    - 典型的な曖昧語を軽く具体化（最小限）
    """
    t = (text or "").strip()
    t = t.translate(_ZEN2HAN_TABLE)
    t = re.sub(r"\s+", " ", t)

    # 軽い具体化
    t = re.sub(r"四隅", "四隅（各角）", t)
    t = re.sub(r"大きめ|小さめ", "適切なサイズ（必要ならパラメータ化）", t)
    t = re.sub(r"適当に|いい感じに", "明示的な数値や規則に基づいて", t)
    return t

def ensure_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def _decide_base_in_path() -> Optional[str]:
    """元コード選択ロジックを元の仕様のまま再現"""
    in_path = get_input_py_path()
    if not in_path:
        if get_use_previous_base():
            if os.path.exists("out.py"):
                in_path = "out.py"
        else:
            if os.path.exists("data/sample1.py"):
                in_path = "data/sample1.py"
    return in_path

def _decode_bytes(b: bytes) -> str:
    for enc in ("utf-8", "cp932", locale.getpreferredencoding(False), "mbcs", "latin-1"):
        try:
            return b.decode(enc)
        except Exception:
            pass
    # 最後の保険
    return b.decode("utf-8", errors="replace")

# === 追加: out.pyの退避 ===
def _rotate_out_py_before_write(output_path: str, versions_dir: str = "out_versions") -> Optional[str]:
    if not os.path.exists(output_path):
        return None
    os.makedirs(versions_dir, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    sha = _sha12_from_file(output_path)
    archived = os.path.join(versions_dir, f"out_{ts}_{sha}.py")
    shutil.move(output_path, archived)
    return archived

def _retention_cleanup(versions_dir: str = "out_versions", keep: int = 20):
    files = sorted(
        glob.glob(os.path.join(versions_dir, "out_*.py")),
        key=lambda p: os.path.getmtime(p),
        reverse=True
    )
    for old in files[keep:]:
        try:
            os.remove(old)
        except Exception:
            pass

def _sha12_from_file(py_path: str) -> str:
    with open(py_path, "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()[:12]

def _extract_explanation_from_query_stdout(stdout_text: str) -> str:
    """
    実行ログから「スクリプトの説明」だけを抜き出す。
    - "--- Script Explanation ---" 行を起点に、それ以降の本文を次の区切りまで取得
    - 区切り候補: 次の '---' ライン, 次の Markdown 見出し, 'Wrote out.py' など
    - 代替: "### スクリプトの説明" セクション
    """
    if not stdout_text:
        return ""

    # 改行を正規化（Windowsの\r\nを\nへ）
    s = stdout_text.replace("\r\n", "\n").replace("\r", "\n")
    print("log:\n"+s)
    # 1) 英語版ヘッダ（行単位マッチ）
    m = re.search(r"(?im)^[ \t]*---\s*Script\s+Explanation\s*---[ \t]*$", s)
    if m:
        tail = s[m.end():].lstrip()

        # 次の区切り候補を探す
        end_candidates = []
        # 次の '--- something ---' ライン
        m2 = re.search(r"(?im)^[ \t]*---.*?---[ \t]*$", tail)
        if m2: end_candidates.append(m2.start())
        # 次の Markdown 見出し
        m3 = re.search(r"(?m)^\s*#{1,6}\s+", tail)
        if m3: end_candidates.append(m3.start())
        # ランタイム末尾によく出る行
        m4 = re.search(r"(?m)^\s*Wrote\s+out\.py.*$", tail)
        if m4: end_candidates.append(m4.start())

        end = min(end_candidates) if end_candidates else len(tail)
        return tail[:end].strip()

    # 2) 日本語Markdownセクション "### スクリプトの説明"
    m = re.search(r"(?im)^###\s*スクリプトの説明\s*$", s)
    if m:
        tail = s[m.end():].lstrip()
        # 次の見出しまで
        mnext = re.search(r"(?m)^\s*#{1,6}\s+", tail)
        end = mnext.start() if mnext else len(tail)
        return tail[:end].strip()

    # 3) 最後の保険：'Script Explanation' の行を起点に、それ以降を全部
    m = re.search(r"(?im)Script\s+Explanation\s*", s)
    if m:
        return s[m.end():].strip()

    # 4) さらなる保険：'Answer' の行を起点に、それ以降を全部
    m = re.search(r"(?im)Answer\s*", s)
    if m:
        return s[m.end():].strip()

    return ""


def _read_doc_or_header_comment(py_path: str) -> str:
    """
    out.py からモジュールドックストリング or 先頭コメント群を要約として拾う
    """
    import ast
    try:
        with open(py_path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        try:
            mod = ast.parse(text)
            doc = ast.get_docstring(mod)
            if doc:
                return doc.strip()
        except Exception:
            pass
        # 先頭コメント
        header_lines = []
        for line in text.splitlines():
            if line.lstrip().startswith("#"):
                header_lines.append(line.lstrip("# ").rstrip())
            elif line.strip() == "":
                if header_lines:
                    header_lines.append("")
            else:
                break
        return "\n".join(header_lines).strip()
    except Exception:
        return ""

def _format_gui_summary(instruction: str, base_for_query: str | None, script_expl: str, output_path: str) -> str:
    mode = "編集" if (base_for_query and os.path.exists(base_for_query)) else "新規"
    base_name = os.path.basename(base_for_query) if (base_for_query and os.path.exists(base_for_query)) else "-"
    parts = [
        "【命令】",
        instruction or "(空)",
        "",
        "【動作形態】",
        f"{mode}" + (f"（基底: {base_name}）" if mode == "編集" else ""),
        "",
        "【スクリプトの説明】",
        script_expl.strip() or "(説明なし)",
    ]
    return "\n".join(parts)



def main(output_path: str = "out.py") -> str:
    """
    前処理（曖昧表現の調整）→ query0929.py を CLI 実行（引数2つ） → out.py の存在確認 → ログ保存
    戻り値: explanation(str) ＝ query0929.py の標準出力（抜粋）
    """
    # 指示テキスト（前処理）
    raw_instruction = get_instruction_text()
    instruction = normalize_instruction(raw_instruction)
    #print(instruction)

    # 元コードパスの決定（未指定時は従来ロジック）
    in_path = _decide_base_in_path() or ""
    new_out_tmp = output_path + ".new.tmp"         # ★ 子プロセスの出力先（一時）

    # もし out.py を参照元として使うなら、一時的にコピーを作ってそれを渡す
    base_for_query = in_path
    using_out_as_base = (
        in_path and os.path.exists(output_path) and
        os.path.abspath(in_path) == os.path.abspath(output_path)
    )
    if using_out_as_base:
        tmp_base = output_path + ".base.tmp"
        shutil.copy2(output_path, tmp_base)
        base_for_query = tmp_base
    else:
        tmp_base = None

    # === CLI 実行 ===
    ROUTE = "hybrid"  # ご指定どおり固定

    # query スクリプトの場所を自動検出（query0929.py 優先）
    this_dir = os.path.dirname(os.path.abspath(__file__))
    cand = [os.path.join(this_dir, "query0929.py"),
            os.path.join(this_dir, "query.py")]
    query_script = next((p for p in cand if os.path.exists(p)), None)
    if not query_script:
        raise FileNotFoundError("query0929.py / query.py が見つかりません。run_pipeline.py と同じディレクトリに置いてください。")

    cmd = [sys.executable, query_script]

    if base_for_query and os.path.exists(base_for_query):
        # 既存スクリプト編集モード:  python <file_path> "<edit>" hybrid
        cmd += [base_for_query, instruction, ROUTE]
    else:
        # 新規スクリプト生成モード:  python "<question>" hybrid
        cmd += [instruction, ROUTE]

    # 直接 out.py に書かせず一時ファイルへ（query 側が --output 対応の場合）
    cmd += ["--output", new_out_tmp]

    # デバッグ表示（必要ならコメントアウト可）
    print("[run_pipeline] exec:", " ".join(repr(x) for x in cmd))

    # 子プロセス側の標準出力文字化けを抑制
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    # バイナリで取得して手動デコード（混在対策）
    proc = subprocess.run(cmd, capture_output=True, text=False, env=env)


    explanation = _decode_bytes(proc.stdout).strip()
    stderr_text = _decode_bytes(proc.stderr).strip()

    new_ready = os.path.exists(new_out_tmp)        # ★ 新規生成の有無

    if (proc.returncode != 0) or (not new_ready):
        # 失敗：何も壊さない（out.py はそのまま）
        err_msg = []
        err_msg.append("[run_pipeline] query.py 実行に失敗しました。")
        err_msg.append(f"returncode={proc.returncode}")
        if explanation: err_msg.append("--- stdout (query0929.py) ---\n" + explanation)
        if stderr_text: err_msg.append("--- stderr (query0929.py) ---\n" + stderr_text)
        msg = "\n".join(err_msg)
        print(msg)
        explanation = (explanation + ("\n\n" + msg if msg else "")).strip()
        # 後片付け
        if os.path.exists(new_out_tmp): os.remove(new_out_tmp)
        if tmp_base and os.path.exists(tmp_base): os.remove(tmp_base)
        out_exists = os.path.exists(output_path)

    else:
        # 成功：旧 out.py をアーカイブ → 新規を out.py へ差し替え
        if os.path.exists(output_path):
            _rotate_out_py_before_write(output_path)  # ★ ここで初めて退避
        shutil.move(new_out_tmp, output_path)
        _retention_cleanup("out_versions", keep=20)
        out_exists = True
        # 後片付け
        if tmp_base and os.path.exists(tmp_base): os.remove(tmp_base)

        # ここで GUI 向けの軽量説明に差し替え
    explanation_raw = explanation  # これまで作ってきた生stdout等（変数名が別ならそちらを）
    script_expl = _extract_explanation_from_query_stdout(explanation_raw)
    if (not script_expl) and os.path.exists(output_path):
        script_expl = _read_doc_or_header_comment(output_path)

    explanation = _format_gui_summary(
        instruction=instruction,
        base_for_query=base_for_query if (base_for_query and os.path.exists(base_for_query)) else None,
        script_expl=script_expl,
        output_path=output_path
    )



    # === セッションログ保存（元ファイルのロジックを維持） ===
    log_dir = get_log_dir()
    ensure_dir(log_dir)
    session_file = os.path.join(log_dir, f"session_{datetime.date.today().isoformat()}.jsonl")

    now = datetime.datetime.now().isoformat(timespec="seconds")
    out_hash = sha1(open(output_path, "r", encoding="utf-8").read()) if out_exists else "-"

    def save_chatlog(session_path: str, record: Dict[str, Any]):
        with open(session_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    # 入力（前処理済み）と実行結果の要約を保存
    save_chatlog(session_file, {"ts": now, "role": "user", "content": instruction})
    save_chatlog(session_file, {
        "ts": now, "role": "assistant", "content": explanation,
        "out_file": output_path if out_exists else None,
        "out_hash": out_hash
    })

    if out_exists:
        print(f"Wrote {output_path}")
    return explanation

if __name__ == "__main__":
    main()
