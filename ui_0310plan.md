# UI プログラム実装計画

## Context

`Chatbot_interface_test.py` は `tkinterdnd2` を使用しているため、Pythonバージョンによって動作しない問題がある。
`query.py` のファイル添付・指示入力・モデル選択・参考スクリプト添付を UI から操作できる新しいUIプログラムを作成する。
`run_pipeline.py` を経由せず、**`ui.py` から `query.py` を直接サブプロセス呼び出しする**構成とする。`tkinterdnd2` を排除する。

---

## 作成・変更ファイル

| ファイル | 操作 |
|---|---|
| `ui.py` | 新規作成（メインUI） |

`run_pipeline.py` は変更しない。

---

## `query.py` の CLI インターフェース（接続仕様）

`query.py` は `if __name__ == "__main__"` ブロック内にのみ argparse があるため、
**インポートして関数を呼ぶことはできない。サブプロセスとして呼び出す。**

```
python query.py <first_arg> <instruction> [オプション]
```

| 引数 | 種別 | 説明 |
|---|---|---|
| `first_arg` | 位置引数 | 編集対象ファイルパス（新規生成時でも何らかのパスが必要） |
| `instruction` | 位置引数 | 編集指示テキスト |
| `-o / --output` | オプション | 出力先ファイルパス |
| `-r / --reference` | オプション | 参考スクリプトパス |
| `--model` | オプション | `gpt` / `gemini`（デフォルト: `gpt`） |
| `--pipeline-mode` | オプション | `off` / `two` / `three`（デフォルト: `three`） |

---

## 実装方針

### 1. `ui.py` の新規作成

#### UI レイアウト（上から順）

```
┌──────────────────────────────────────────────────────────────┐
│  LLM スクリプト生成インターフェース                           │
├──────────────────────────────────────────────────────────────┤
│  命令テキスト                                                  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ （テキスト入力エリア、8行）                              │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  対象ファイル: [sample.py          ] [ ファイルを選択 ] [×]  │
│  参考スクリプト: [ref.py           ] [ ファイルを選択 ] [×]  │
│                                                               │
│  モデル: [gpt ▼]   ☐ 継続編集モード（out.py を基底にする）  │
│                                                               │
│  [ 実  行 ]   [ リセット（履歴クリア） ]                     │
│                                                               │
│  ステータス: 準備完了                                         │
│                                                               │
│  対話ログ（変更点・理由など）                                  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ （ログ表示エリア、22行、readonly）                       │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

#### 主要コンポーネント

| 変数名 | 種類 | 説明 |
|---|---|---|
| `entry` | `tk.Text` (8行) | 命令テキスト入力 |
| `main_file_var` | `tk.StringVar` | 対象ファイルパス表示 |
| `ref_file_var` | `tk.StringVar` | 参考スクリプトパス表示 |
| `model_var` | `tk.StringVar` | モデル選択 ("gpt" / "gemini") |
| `use_prev_var` | `tk.IntVar` | 継続編集モード checkbox |
| `chat_log` | `tk.Text` (22行) | ログ表示（disabled） |
| `status_label` | `tk.Label` | ステータス表示 |
| `button` | `tk.Button` | 実行ボタン |
| `result_q` | `queue.Queue` | ワーカー→GUI受け渡し |

#### ファイル選択ロジック

```python
def select_main_file():
    path = filedialog.askopenfilename(
        filetypes=[("Pythonファイル", "*.py"), ("テキストファイル", "*.txt"), ("全ファイル", "*.*")]
    )
    if path:
        main_file_var.set(path)

def clear_main_file():
    main_file_var.set("")
```
参考スクリプトも同様。

#### ワーカー関数（スレッド実行）

`run_pipeline.py` は使わず、`query.py` へのサブプロセス呼び出しを `ui.py` 内で直接構築する。

```python
def _worker_run_pipeline(instruction_text, main_path, ref_path, model, use_prev):
    import sys, os, subprocess, shutil, datetime, json

    OUTPUT_PATH = "out.py"
    new_out_tmp = OUTPUT_PATH + ".new.tmp"

    # --- 継続編集モードのロジック（run_pipeline._decide_base_in_path 相当） ---
    if main_path and os.path.exists(main_path):
        first_arg = main_path
    elif use_prev and os.path.exists(OUTPUT_PATH):
        # out.py を一時コピーして渡す（query.py が上書きしないよう保護）
        tmp_base = OUTPUT_PATH + ".base.tmp"
        shutil.copy2(OUTPUT_PATH, tmp_base)
        first_arg = tmp_base
    else:
        first_arg = ""  # query.py 側の load_script_files が空文字を許容する前提

    query_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "query.py")

    cmd = [sys.executable, query_script, first_arg, instruction_text]
    cmd += ["--output", new_out_tmp]
    cmd += ["--model", model]
    if ref_path and os.path.exists(ref_path):
        cmd += ["--reference", ref_path]

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    proc = subprocess.run(cmd, capture_output=True, text=False, env=env)
    stdout = proc.stdout.decode("utf-8", errors="replace").strip()
    stderr = proc.stderr.decode("utf-8", errors="replace").strip()

    # tmp_base の後片付け
    if "tmp_base" in dir() and os.path.exists(tmp_base):
        os.remove(tmp_base)

    if proc.returncode != 0 or not os.path.exists(new_out_tmp):
        msg = f"[ERROR] returncode={proc.returncode}\n{stderr or stdout}"
        result_q.put(("error", msg))
        if os.path.exists(new_out_tmp):
            os.remove(new_out_tmp)
        return

    # 成功：旧 out.py をアーカイブ → 差し替え
    if os.path.exists(OUTPUT_PATH):
        _rotate_out_py(OUTPUT_PATH)
    shutil.move(new_out_tmp, OUTPUT_PATH)

    # ログ保存
    _save_chatlog(instruction_text, stdout)

    result_q.put(("ok", stdout))
```

#### 継続編集モードのロジック詳細

| 条件 | `first_arg` に渡す値 |
|---|---|
| 対象ファイルが指定されている | `main_path` |
| 継続編集モード ON かつ `out.py` が存在する | `out.py` の一時コピー (`out.py.base.tmp`) |
| どちらでもない | 空文字（新規生成として `query.py` に任せる） |

`out.py` を直接渡さず一時コピーを渡す理由：`query.py` が `--output` に同一パスを受け取るケースで上書き競合が起きないようにするため。

#### ログ保存（`_save_chatlog`）

`run_pipeline.py` が行っていたセッションログ保存を `ui.py` 側で担う。

```python
def _save_chatlog(instruction: str, response: str):
    import json, datetime, os
    log_dir = "chatlogs"
    os.makedirs(log_dir, exist_ok=True)
    session_file = os.path.join(log_dir, f"session_{datetime.date.today().isoformat()}.jsonl")
    now = datetime.datetime.now().isoformat(timespec="seconds")
    with open(session_file, "a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": now, "role": "user", "content": instruction}, ensure_ascii=False) + "\n")
        f.write(json.dumps({"ts": now, "role": "assistant", "content": response}, ensure_ascii=False) + "\n")
```

#### out.py のアーカイブ（`_rotate_out_py`）

`run_pipeline._rotate_out_py_before_write` 相当を `ui.py` 内に移植する。

```python
def _rotate_out_py(output_path: str, versions_dir: str = "out_versions"):
    import shutil, hashlib, datetime, os
    os.makedirs(versions_dir, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(output_path, "rb") as f:
        sha = hashlib.sha1(f.read()).hexdigest()[:12]
    shutil.move(output_path, os.path.join(versions_dir, f"out_{ts}_{sha}.py"))
```

#### ポーリング・ログ表示

`Chatbot_interface_test.py` の `_poll_queue()` パターンをそのまま継承。
`root.after(50, _poll_queue)` で20fps更新。

#### エラーハンドリング

`result_q.put(("error", msg))` を受け取った場合、ステータスラベルに赤字でエラーを表示し、実行ボタンを再度有効化する。

#### スレッド安全性

実行中は `button` を `DISABLED` にする。リセットボタンも実行中は `DISABLED` にし、完了・エラー後に `NORMAL` へ戻す。

---

## 既存パターンの再利用

- `run_function()` / `_worker_run_pipeline()` / `_poll_queue()` の非同期パターン → そのまま踏襲
- `chat_log` の継続編集モード（区切り線挿入・行数上限600）→ 同一ロジック
- `reset_function()` → 同一ロジック（ファイルパス変数もクリア）

---

## 削除・排除

- `tkinterdnd2` のインポートを完全に除去
- ドロップエリア (`drop_area`) を除去
- `drop()` 関数を除去
- `run_pipeline.py` の injectable 関数パッチ方式を除去（`run_pipeline` は一切インポートしない）
- `get_history` 概念を除去（`query.py` に会話履歴の概念がないため）

---

## 検証手順

1. `python ui.py` で起動確認（tkinterdnd2 なしで起動できること）
2. ファイル選択ボタン → ダイアログが開き、パスが表示されること
3. 参考スクリプト選択ボタンも同様
4. モデルドロップダウンで gpt/gemini を切り替えできること
5. 「実行」ボタンを押して `query.py` が直接サブプロセスとして呼ばれること（`run_pipeline` が呼ばれないこと）
6. ログエリアに説明が表示されること
7. 継続編集モード ON → `out.py` が存在する場合に `first_arg` として渡されること
8. リセットボタンでファイルパス・ログがクリアされること
9. 実行中はボタンが無効化され、完了後に再有効化されること
10. エラー時（`returncode != 0`）にステータスラベルにエラーが表示されること
