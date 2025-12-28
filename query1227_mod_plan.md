# query1227.py 修正計画書（スクリプト実行→エラー解析→再生成ループの追加）

## 1. 目的
- **生成したEvoShip用Pythonスクリプトを自動実行し、実行エラー（特に `CreateBracket` 周辺の COM 例外）を検知したら、LLM に「失敗箇所のブラケットパラメータだけ」を中心に再生成（修正）させる**処理を `query1227.py` に追加する。
- `query1226.py` には「生成→保存→実行→失敗→LLM修正→再実行」の骨格があるため、同等の枠組みを `query1227.py` に移植しつつ、**ブラケットパラメータに特化したプロンプト設計**に差し替える。

---

## 2. 現状整理

### 2.1 query1227.py（現状）
- GraphRAG（Neo4j）で回答（= スクリプト＋説明）を生成し、`-o/--output` 指定時に **ファイル保存まで**を実施。
- **生成スクリプトの実行**と、**実行エラーを入力として再生成**する自己修正ループがない。
- 既に Neo4j の Cypher エラーに対するリトライ（`execute_graph_qa(..., is_retry=True)`）はあるが、**Pythonスクリプト実行の失敗**は扱っていない。

### 2.2 query1226.py（参考になる点）
- `run_script(script_path)` を持ち、`subprocess.run` で生成スクリプトを実行し、`stderr` を取得。
- `MAX_RETRIES` と `fix_code(code, error_message)` により、**実行エラー→LLM修正→再実行**のループがある（ただしプロンプトは汎用）。

---

## 3. 追加する処理フロー（To-Be）
`query1227.py` に以下のステップを追加する。

1. **(Attempt 0)** GraphRAG でスクリプト生成 → `output_path` に保存  
2. `run_script(output_path)` で **実行**（タイムアウト付き）  
3. 成功なら終了  
4. 失敗なら `stderr`（Traceback）を解析し、**ブラケット関連の失敗コンテキスト**を抽出  
5. **(Attempt 1..N)** LLM に「最小変更での修正」を指示してスクリプト再生成 → 保存 → 再実行  
6. `MAX_RETRIES` まで繰り返し、最後まで成功しない場合はログと最終失敗スクリプトを残して終了

> ポイント：**再生成のたびに「全コードを書き直させる」より、「エラー周辺のブラケットパラメータを局所修正」させる方が成功率が上がる**。そのため、プロンプトは「変更範囲を強制」し、参照すべき情報を「エラー行の前後と該当パラメータ定義」に寄せる。

---

## 4. 実装方針（query1227.pyへの具体的追加）

### 4.1 追加関数：run_script（query1226.py から移植）
- `import subprocess` を追加
- 生成スクリプトを `sys.executable` で起動し、`capture_output=True, text=True, timeout=...` で結果を取得
- 戻り値は以下を推奨：
  - `success: bool`
  - `stdout: str`
  - `stderr: str`
  - `returncode: int`

**注意（EvoShip/COM前提）**
- COM 初期化や GUI 依存でハングする場合があるため、**timeout を必須化**（例: 30〜120秒、CLIで指定可能にする）。
- 実行環境が Windows/Powershell であるため、`sys.executable` 実行で十分だが、必要なら `creationflags`（別コンソール抑制等）も後から検討する。

---

### 4.2 追加関数：parse_traceback / extract_bracket_failure_context
COM 例外は `pywintypes.com_error` のように **情報量が少ない**ため、LLM に渡す情報を増やす工夫が必要。

#### (A) Traceback から最低限抽出する項目
- 失敗した **ファイルパス**（基本は output_path）
- 失敗した **行番号**（例：`line 905`）
- 失敗した **行のコード**（例：`bracketC1 = part.CreateBracket(bracketPramC1,False)`）
- 例外クラス名（例：`pywintypes.com_error`）
- 例外引数（可能ならそのまま文字列で）

#### (B) スクリプト本文から抽出する項目（局所コンテキスト）
- 失敗行の **前後 N 行**（推奨：前後 50 行程度）
- 失敗行に登場する `bracketParam` 変数名（例：`bracketPramC1`）
- その `bracketParam` の **定義ブロック**（辞書/オブジェクト生成/フィールド代入の連続部分を可能な限り拾う）
- 同一ブロック内で参照される `profileXX`, `solidX`, `faces`, `Surfaces1/2` に相当する変数の定義（見つかる範囲）

> 実装は「完璧なAST解析」より、まずは **正規表現＋行ベース**でよい。  
> 例：`bracketPramC1` というトークンの出現位置から上方向に「直近の代入/辞書定義」を探し、一定行数で打ち切る。

---

### 4.3 修正ループの組み込み位置
- `if args.output:` で script を保存した直後に、以下を追加する：
  - `success, stdout, stderr, rc = run_script(output_path)`
  - `if not success: ...` で **再生成ループ**へ

---

### 4.4 追加するCLIオプション（推奨）
- `--max-retries`（既定：3）
- `--timeout-sec`（既定：60）
- `--keep-attempts`（既定：ON；各試行のスクリプトを `xxx.attempt1.py` のように保存）
- `--no-exec`（既定：OFF；実行せず保存だけしたい時のため）

---

## 5. LLM再生成プロンプト設計（ブラケットパラメータ特化）

### 5.1 なぜ「汎用修正」では弱いか
- `pywintypes.com_error` は詳細な原因を返さないことが多く、LLM が「何を直すべきか」を特定しにくい。
- そのため、**“どのブラケットパラメータがどんな形で定義され、どの面ペアを結んでいるか”** を明示し、**変更可能な範囲を狭く**して探索させる。

---

### 5.2 基本戦略：最小変更ポリシー（強制）
再生成プロンプトでは必ず以下を強制する。

- **変更対象は「エラー行の CreateBracket に渡している bracketParam の定義と、それに直結する補助変数」だけ。**
- それ以外のコード（生成された形状、部材生成順序、他のブラケット）は **原則そのまま**。
- どうしても周辺の参照（faces の取り方等）を直す必要がある場合でも、変更は **エラー行の前後ブロック内に限定**。
- 出力は **完成した全スクリプト**（省略なし、` ```python ... ``` ` で囲む）。

---

### 5.3 ブラケット特化の修正観点（LLMに渡す“探索軸”）
LLMに「どこをどう疑うべきか」を明示する（重要）。

1. **Surfaces1 / Surfaces2 の妥当性**
   - 参照している面が None/未生成/型不一致になっていないか
   - 面ペア順序（PLS↔FL 等）が参考スクリプトと整合するか
2. **BaseElement の妥当性**
   - 原則 `profileXX[0]`（Profile本体）を使う、solid を渡していないか
3. **End1/End2 と EndElements**
   - `AddEnd1Elements/AddEnd2Elements` に対応する要素が欠けていないか
4. **BracketType とフィールドの整合**
   - 参考スクリプトに存在する `BracketType` / `Sf1EndElements` / `Sf2EndElements` を勝手に増減しない  
   - 型により必須フィールドが違う可能性があるため、参考スクリプトで同型を優先
5. **寸法の符号・範囲**
   - Height/Width/Thickness が 0 以下になっていないか
   - 板厚に対して極端に大きすぎ/小さすぎの値になっていないか（可能なら参照部材寸法から再計算）
6. **向き（Orientation/Vector）が必要な型の場合**
   - 参照面の法線に対して不正な向きになっていないか  
   - 参考スクリプトに合わせた規約（例えば FL を基準にする等）を踏襲

> 上記をプロンプトで「チェックリスト」として提示し、LLMが “見当違いの大改造” をしないように誘導する。

---

### 5.4 推奨プロンプト構造（修正専用テンプレート案）
`query1226.py` の `FIX_TEMPLATE` を置き換える形で、以下のようなテンプレートを `query1227.py` に追加する。

- **入力**：`full_code`, `stderr`, `error_line_info`, `local_context`, `reference_snippet(optional)`
- **出力**：` ```python ... ``` ` のみ（説明不要）

テンプレート骨子（例）：

- 失敗情報（Traceback）をそのまま添付
- 失敗行（1行）と前後N行（コンテキスト）
- 対象 bracketParam の定義ブロック（抜粋）
- 参考スクリプトから「同系の CreateBracket」例（あれば抜粋）
- 修正ルール（最小変更、未知フィールド追加禁止、全コード出力、省略禁止）

---

### 5.5 追加の工夫：2段階生成（任意・成功率向上）
COMエラーのように曖昧な場合、**いきなり全コード再生成**より以下が安定することが多い。

1) LLMに「修正案」を **JSON** で出させる  
   - 例：`{"target_param":"bracketPramC1","changes":{"Height":..., "Surfaces1":...}}`
2) Python側で該当箇所だけ機械的に反映（正規表現 or ASTパッチ）  
3) それでもダメなら、最終手段として全コード再生成

> ただし今回は「まず query1226 に合わせて全コード再生成」を第一目標とし、2段階方式は拡張として計画に含める。

---

## 6. ログ保存設計（デバッグ効率を上げる）
再生成ループでは情報が消えやすいので、以下を推奨。

- 各試行でファイルを分けて保存：
  - `output.py`（常に最新）
  - `output.attempt0.py`, `output.attempt1.py`, ...
- エラーログ保存：
  - `output.attempt1.stderr.log` のように `stderr` を保存
- 失敗コンテキスト（抽出結果）も JSON で保存（任意）：
  - `output.attempt1.context.json`

---
