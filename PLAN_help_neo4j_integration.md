# Plan: ./help HTML & ブラケット知識の Neo4j 統合

## Context

現在のシステムは API 仕様書（`./data/api*.txt`）のみを Neo4j に構築しており、`./help` の HTML ドキュメント（約300ファイル）は未利用。ブラケット生成に必要なブラケット種別一覧や接続型ルールは `./prompts/` から毎回 LLM に静的渡しで対応している。

**課題:**
- `bracket_type_reference.md`（5.1 KB）が毎回のブラケットタスクでコンテキストに丸ごと挿入されている
- Help HTML の知識（UI操作説明・パラメータ解説）がグラフから検索不可
- BracketType と ScriptExample ノードの間に意味的リンクが存在しない

**目的:** Help HTML を Neo4j に取り込み、BracketType enum を構造化ノードとして移行することで、クエリ精度と LLM コンテキスト効率を改善する。

---

## 推奨アプローチ: 3ステップ段階的拡張

### Step 1: Help HTML → Neo4j（優先度: 高）

**新ノード型:**

```
HelpPage {id, file_name, title, page_type, summary, keywords[], raw_text, source="help"}
```

- `page_type`: ファイル名プレフィックスで自動判定（`cmd_`/`about_`/`sample_`）
- `keywords` / `summary`: Tier1（短い `cmd_` ページ）はノーLLM（タイトル・本文から機械的に生成）、Tier2（`about_`/`sample_`/長文）のみバッチLLMでスキーマ指定抽出
- **`HelpSection` は採用しない**: `_retrieve_help_context()` のクエリは `HelpPage` の `summary` / `keywords` のみ参照するため、セクション粒度のノードは死蔵になる。ページ単位の粒度で十分。

**新リレーション:**

```
(HelpPage) -[:DESCRIBES]->  (Object | Method)  ← ファイル名→APIノード名マッチング
(HelpPage) -[:RELATED_TO]-> (HelpPage)          ← HTML内 href から自動生成
(HelpPage) -[:DEFINES]->    (BracketShapeType)  ← Step 2 と連携
```

**DESCRIBES リンク生成戦略:**
- Technique A（決定論的）: `cmd_ship_bracket.html` → `bracket` を含む Object/Method を検索・リンク
- Technique C（LLM、小規模）: `about_` ページ約50件のみ LLM でマッチング

### Step 2: BracketType 構造化ノード移行（優先度: 高）

`prompts/bracket_type_reference.md` のマークダウンテーブルを正規表現でパースし、構造化ノードとして Neo4j に格納。

**新ノード型:**

```
BracketShapeType {id, bracket_type(int), shape_name, bracket_params[], category, usage_note}
DimensionType    {id, dim_type(int), shape_name, params[], is_default_sf1, is_default_sf2}
```

**新リレーション:**

```
(HelpPage) -[:DEFINES]->      (BracketShapeType)
(BracketShapeType) -[:USES_DIM_TYPE]-> (DimensionType)
```

**注:** `bracket_domain_rules.md` の手続きルール（「第2引数は必ずFalse」等）は引き続き `./prompts/` に置く。ルールは LLM への散文として機能するもので、グラフノード化しても検索精度に寄与しない。

### Step 3: クエリ層の拡張（優先度: 中）

`query_graph.py` に `_retrieve_help_context()` 関数を追加。`ask()` 呼び出し前にキーワードマッチで関連ヘルプページを取得し、コンテキストに追加。

```python
def _retrieve_help_context(question: str, graph) -> str:
    # is_bracket_task() が True のとき BracketShapeType + cmd_ship_bracket ページを取得
    # その他の場合はキーワードで HelpPage を検索
    cypher = """
    MATCH (h:HelpPage)
    WHERE any(kw IN h.keywords WHERE toLower(kw) CONTAINS toLower($term))
       OR toLower(h.title) CONTAINS toLower($term)
    RETURN h.title, h.summary LIMIT 5
    """
```

---

## データフロー（既存パイプライン再利用 + インクリメンタル挿入）

### 既存 API/スクリプト ingest（変更なし）
```
api*.txt / *.py → LLM抽出 → _triples_to_graph_documents() → Neo4j 全削除 → add_graph_documents()
```

### Help HTML ingest（新規、10ファイルバッチ処理）
```
10ファイルごとにループ:
  BeautifulSoup パース（LLM不要）
      ↓ Tier1: soup.get_text(separator="\n") でプレーンテキスト抽出
      ↓ Tier2: html2text ライブラリで Markdown に変換（テーブル構造を保持）
  [Tier2のみ] LLM 1コール per 8ファイル — スキーマ指定によるノード・リレーション抽出
      ↓  ※ LLM には Markdown 変換済みテキスト + グラフスキーマ定義を渡す
      ↓  ※ LLM は { "nodes": [...], "relationships": [...] } 形式で出力
  _triples_to_graph_documents()  ← LLM不使用、変換のみ
      ↓
  graph.add_graph_documents()    ← LLM不使用、MERGEで追記（削除しない）
```

**HTML テキスト変換方針:**
- **Tier1（`cmd_` ページ）**: `soup.get_text(separator="\n")` のみ。LLM 不使用なので変換精度は問わない
- **Tier2（`about_` / `sample_` / 長文）**: `html2text` ライブラリで Markdown 変換してから LLM に渡す。`<table>` が `| ... |` 形式に変換されるため、パラメータ表（BracketType 一覧等）の LLM 読み取り精度が向上する
  ```python
  import html2text
  h = html2text.HTML2Text()
  h.ignore_links = True
  md_text = h.handle(html_content)  # テーブルも Markdown 表に変換
  ```
- `HelpPage.raw_text` には Tier 問わずこの変換済みテキストを格納する

**Tier2 LLM プロンプトのスキーマ指定:**

LLM には以下のスキーマを提示し、`_extract_graph_from_specs_with_llm()` と同じ JSON 形式で出力させる。

```
【許可するノード型】
- HelpPage  {id, file_name, title, page_type, summary, keywords[]}
  ※ id = file_name（例: "about_ship_settings"）
- Object    {id, name}   ← 既存ノードへの参照のみ（新規作成しない）
- Method    {id, name}   ← 既存ノードへの参照のみ（新規作成しない）
- BracketShapeType {id, bracket_type, shape_name}  ← 既存ノードへの参照のみ

【許可するリレーション型】
- (HelpPage) -[:DESCRIBES]->  (Object | Method)     ← ページが説明するAPI要素
- (HelpPage) -[:DEFINES]->    (BracketShapeType)    ← ブラケット型の定義ページ

【出力形式】
{"nodes": [...], "relationships": [...]}
※ Object / Method / BracketShapeType は relationships の参照用のみ記述。HelpPage ノードのみ新規作成する。
```

LLM 出力後、`add_graph_documents()` の前に許可ノード型でフィルタするバリデーションを挟む（スキーマ外のノード型を除去）。これにより `_retrieve_help_context()` の Cypher クエリが想定通りのスキーマに沿って動作することを保証する。

**ポイント:**
- `_triples_to_graph_documents()` と `add_graph_documents()` は **LLM不使用**
- Help ingest は API ingest の **後に実行**（既存データを削除せず MERGE 追記）
- 10ファイルごとにバッチ処理 → メモリ使用量を抑制（300ファイル → 約30回の `add_graph_documents()` 呼び出し）
- LLM は Tier2 ページのスキーマ指定抽出のみ（合計約21コール）

Cypher を直接書くのは以下の2箇所のみ:
- 既存 API ノード名の取得（`MATCH (m:Method) RETURN m.name` など）
- Neo4j インデックス/制約の作成（初回のみ、`CREATE CONSTRAINT ...`）

---

## 実装ファイルと変更内容

| ファイル | 変更内容 |
|---------|---------|
| `ingest0226-1.py` | `_parse_help_directory()`, `_extract_help_summaries_with_llm()`, `_help_pages_to_triples()`, `_parse_bracket_type_reference()` を追加。`_build_and_load_neo4j()` に統合 |
| `query_graph.py` | `_retrieve_help_context()` 追加、`ask()` 内で呼び出し。`CYPHER_GENERATION_TEMPLATE_JP` のスキーマ説明に新ノード型を追記 |
| `prompts/loader.py` | `is_bracket_task()` パターンを参考に `is_help_relevant()` 追加 |

**変更しないファイル:**
- `prompts/bracket_domain_rules.md` ← 手続きルールは現状維持
- `query_hybrid.py`, `query_norag*.py` ← 拡張対象外（必要なら後で）

---

## 実装順序（リスク低い順）

1. **Phase 1**: `_parse_help_directory()` — BeautifulSoup で HTML パース、LLM なし、Neo4j 書き込みなし。出力確認後に進む。
2. **Phase 2**: `_parse_bracket_type_reference()` — 正規表現で markdown テーブルをパース。LLM なし。
3. **Phase 3**: 決定論的リレーション生成（Technique A + href クロスリファレンス）
4. **Phase 4**: Tier2 LLM バッチ抽出（スキーマ指定、約14回 LLM コール、コスト限定）
5. **Phase 5**: Neo4j 統合（`_build_and_load_neo4j()` に組み込み、`ingest.py` 実行）
6. **Phase 6**: `query_graph.py` クエリ層更新

---

## 検証方法

```bash
# Phase 1: パース動作確認（Neo4j 未使用）
python -c "from ingest import _parse_help_directory; from pathlib import Path; pages = _parse_help_directory(Path('help')); print(len(pages), 'pages found'); print(pages[0])"

# Phase 2: ブラケット型パース確認
python -c "from ingest import _parse_bracket_type_reference; from pathlib import Path; nodes = _parse_bracket_type_reference(Path('prompts/bracket_type_reference.md')); print(len(nodes), 'types found'); print(nodes[0])"

# Phase 5: フル ingest 実行
python ingest.py

# Phase 5 後: Neo4j に新ノードが存在することを確認
# Neo4j Browser で: MATCH (h:HelpPage) RETURN count(h)
# 期待値: ~300
# MATCH (bt:BracketShapeType) RETURN count(bt)
# 期待値: ~18（BracketType 種別数）

# Phase 6: クエリ動作確認
python query_graph.py ./script/sample.py "ブラケットをつけてください。" -o ./script/output.py
# → help context が取得されログに表示されることを確認
```

---

## コスト見積もり

| 処理 | LLM コール数 | 備考 |
|------|------------|------|
| API spec 抽出（現状） | ~10 | 変化なし |
| Help Tier2 スキーマ指定抽出 | ~14 | 8ページ/バッチ、約110ページ対象 |
| BracketType パース | 0 | 正規表現のみ |
| Help DESCRIBES（Technique A） | 0 | 決定論的 |
| Help DESCRIBES（Technique C） | ~7 | about_ 50件、7ページ/バッチ |
| **合計追加コール** | **~21** | 1回の ingest で完結 |
