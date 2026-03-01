# Chatbot_interface_test.py
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
import threading, queue
import os
import run_pipeline

# --- グローバル変数 ---
dropped_file_path = None          # ドラッグされたファイルのパス(1つまで)
history = []                      # 会話履歴
use_prev_var = None               # 継続編集モード用チェック状態
result_q = queue.Queue()  # ★追加：ワーカー→GUI 受け渡し用


# --- ドロップ処理 ---
def drop(event):
    global dropped_file_path
    path = event.data.strip("{}")
    if os.path.isfile(path) and (path.endswith(".txt") or path.endswith(".py")):
        dropped_file_path = path
        status_label.config(text=f"ファイル受け取り: {os.path.basename(path)}")
    else:
        status_label.config(text="無効なファイル形式です（.txt または .py）")

# --- 初期化処理 ---
def reset_function():
    global dropped_file_path, history
    dropped_file_path = None
    history = []
    entry.delete("1.0", "end")
    chat_log.delete("1.0", "end")
    status_label.config(text="準備完了")

# --- 実行処理 ---
# def run_function():
#     global dropped_file_path, history
#     instruction_text = entry.get("1.0", "end-1c").strip()
#     if not instruction_text:
#         status_label.config(text="命令テキストが空です")
#         return

#     # run_pipeline の取得関数を動的に上書き
#     run_pipeline.get_input_py_path = lambda: (
#         dropped_file_path if dropped_file_path and dropped_file_path.endswith(".py") else None
#     )
#     run_pipeline.get_instruction_text = lambda: instruction_text
#     run_pipeline.get_history = lambda: history
#     run_pipeline.get_log_dir = lambda: "chatlogs"
#     # チェック状態を反映（ON のときだけ out.py を基底に使用）
#     run_pipeline.get_use_previous_base = lambda: bool(use_prev_var.get())
#     if(not run_pipeline.get_use_previous_base):
        
#         chat_log.delete("1.0", "end")
#     try:
#         explanation = run_pipeline.main(output_path="out.py")

#         # 履歴を更新（コードはファイル保存のため説明のみ保持）
#         history.append({"role": "user", "content": instruction_text})
#         history.append({"role": "assistant", "content": explanation or "(説明なし)"})

#         # 画面ログを更新
#         chat_log.insert("end", f"【要求】\n{instruction_text}\n\n")
#         chat_log.insert("end", "【説明】\n" + (explanation or "(説明なし)") + "\n\n")
#         chat_log.see("end")

#         status_label.config(text="処理完了: out.py を更新。説明は下のログに追記しました。")
#     except Exception as e:
#         status_label.config(text=f"エラー: {e}")

def run_function():
    instruction_text = entry.get("1.0", "end-1c").strip()
    if not instruction_text:
        status_label.config(text="命令が空です")
        return

    # 継続編集フラグ（チェックONなら True）
    continuous_edit = bool(use_prev_var.get())

    # 実行中UI
    status_label.config(text="実行中…")
    button.config(state="disabled")

    # === ログ表示：継続編集なら残す／通常はクリア ===
    chat_log.config(state="normal")
    if not continuous_edit:
        # 通常モード：毎回クリア
        chat_log.delete("1.0", "end")
    else:
        # 継続編集：見やすい区切りだけ挿入（重くならないよう短く）
        import datetime
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        chat_log.insert("end", f"\n── 継続編集: {now} ───────────────────────\n")
        # （任意）履歴が長くなりすぎないように上限を維持
        MAX_LINES = 600
        lines = int(chat_log.index("end-1c").split(".")[0])
        if lines > MAX_LINES:
            chat_log.delete("1.0", f"{lines - MAX_LINES}.0")
    chat_log.config(state="disabled")

    # ここからは従来どおり：非同期起動ならワーカーを回す
    # ※ すでに導入済みの非同期版ならそのままでOK
    t = threading.Thread(
        target=_worker_run_pipeline,
        args=(instruction_text, dropped_file_path, continuous_edit),
        daemon=True
    )
    t.start()



def _worker_run_pipeline(instruction_text: str, dropped_file_path_local: str | None, use_prev: bool):
    """GUIを触らずに重い処理だけを実行。結果はQueueへ。"""
    try:
        import run_pipeline

        # run_pipeline の取得関数を動的に上書き（従来と同じだがGUI側で呼ばない）
        run_pipeline.get_input_py_path = lambda: (
            dropped_file_path_local if (dropped_file_path_local and dropped_file_path_local.endswith(".py")) else None
        )
        run_pipeline.get_instruction_text = lambda: instruction_text
        run_pipeline.get_history = lambda: []  # historyはログ保存用。ここでは不要なら空でOK
        run_pipeline.get_log_dir = lambda: "chatlogs"
        run_pipeline.get_use_previous_base = lambda: bool(use_prev)

        summary = run_pipeline.main(output_path="out.py")  # 軽量サマリが返る前提
        result_q.put(("ok", summary))
    except Exception as e:
        result_q.put(("err", str(e)))

def _poll_queue():
    """Queueに溜まった結果をメインスレッドでUI反映（freeze回避）。"""
    try:
        while True:
            kind, payload = result_q.get_nowait()
            continuous_edit = bool(use_prev_var.get())  # ★ 継続編集フラグ

            # 一度だけ state を open
            chat_log.config(state="normal")

            # 追記内容をまとめて1回だけ insert する（軽量化）
            if kind == "ok":
                text_to_add = (payload or "(説明なし)")
                if continuous_edit:
                    # ログは残す：軽い区切り線だけ入れる
                    import datetime
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    block = f"\n── 継続編集: {now} ───────────────────────\n{text_to_add}\n"
                    chat_log.insert("end", block)
                    # 上限を軽く維持（行数上限）
                    MAX_LINES = 600
                    lines = int(chat_log.index("end-1c").split(".")[0])
                    if lines > MAX_LINES:
                        chat_log.delete("1.0", f"{lines - MAX_LINES}.0")
                else:
                    # 通常：毎回クリアして最新だけ表示
                    chat_log.delete("1.0", "end")
                    chat_log.insert("end", text_to_add)

                status_label.config(text="完了")
                button.config(state="normal")

            elif kind == "err":
                err_text = f"[エラー]\n{payload}"
                if continuous_edit:
                    chat_log.insert("end", "\n── エラー ─────────────────────────────\n" + err_text + "\n")
                    MAX_LINES = 600
                    lines = int(chat_log.index("end-1c").split(".")[0])
                    if lines > MAX_LINES:
                        chat_log.delete("1.0", f"{lines - MAX_LINES}.0")
                else:
                    chat_log.delete("1.0", "end")
                    chat_log.insert("end", err_text)

                status_label.config(text="失敗")
                button.config(state="normal")

            # 閉じるのは最後に1回だけ
            chat_log.config(state="disabled")

    except queue.Empty:
        pass
    # 20fps程度で更新
    root.after(50, _poll_queue)




# --- GUIセットアップ ---
root = TkinterDnD.Tk()
root.title("LLM_スクリプト生成インターフェース試作（会話継続・基底選択）")
root.geometry("780x660")

# 命令テキスト
entry_label = tk.Label(root, text="命令テキスト")
entry_label.pack()
entry = tk.Text(root, width=90, height=8)
entry.pack(pady=5)

# ドロップエリア
drop_area = tk.Label(root, text="スクリプト生成用 .py/.txt 投入口（ドラッグ＆ドロップ）", relief="ridge", width=70, height=4)
drop_area.pack(pady=10)
drop_area.drop_target_register(DND_FILES)
drop_area.dnd_bind('<<Drop>>', drop)

# 継続編集モード（out.py を基底にするかどうか）
mode_frame = tk.Frame(root)
mode_frame.pack(pady=2)
use_prev_var = tk.IntVar(value=0)  # 0: 新規作成, 1: out.py を基底に継続編集
chk = tk.Checkbutton(
    mode_frame,
    text="継続編集モード（直近の out.py を基底にする）",
    variable=use_prev_var
)
chk.pack()

# 実行/リセットボタン
btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)
button = tk.Button(btn_frame, text="実行", command=run_function)
button.grid(row=0, column=0, padx=5)
reset = tk.Button(btn_frame, text="リセット（履歴クリア）", command=reset_function)
reset.grid(row=0, column=1, padx=5)

# ステータス表示
status_label = tk.Label(root, text="準備完了")
status_label.pack(pady=5)

# 対話ログ（説明表示）
log_label = tk.Label(root, text="対話ログ（変更点・理由など）")
log_label.pack()
chat_log = tk.Text(root, width=90, height=22)
chat_log.pack(pady=5)

root.after(50, _poll_queue)  # ★追加：Queueをポーリング開始
root.mainloop()

