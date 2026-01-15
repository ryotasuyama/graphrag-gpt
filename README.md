# GraphRAG GPT

このプロジェクトは、ベクトル検索（Chroma）とグラフ検索（Neo4j）を組み合わせた GraphRAG（Graph Retrieval-Augmented Generation）の実装です。Pythonスクリプトファイル（`data/*.py`）をソースとして、Tree-sitterによる構文解析で知識グラフを構築し、CADアプリケーション「EvoShip」のAPI操作コードを生成・編集できます。

## 🚀 特徴

- ベクトル検索: Chroma + OpenAI Embeddings によるセマンティック検索
- グラフ検索: Neo4j + Cypher 生成チェーンによるグラフQA
- Tree-sitterベースの取り込み: Pythonスクリプトを構文解析し、メソッド呼び出しやデータフローを抽出してグラフを構築
- スクリプト編集機能: 既存のPythonスクリプトを編集指示に基づいて自動修正・生成
- 冪等な再構築: 取り込み時にNeo4jを初期化して再構築（実行毎に同じ結果）

## 📋 前提条件

- Python 3.13.5以上
- Neo4j（ローカルまたはクラウド）
- OpenAI互換APIキー（Embeddings および Chat モデル用）
- Tree-sitter（Python構文解析用）

## 🛠️ セットアップ

### 1. リポジトリのクローン
```bash
git clone <repository-url>
cd graphrag-gpt
```

### 2. 仮想環境の作成と有効化
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate    # Windows
```

### 3. 依存関係のインストール
```bash
pip install -r requirements.txt
```

### 4. 環境変数の設定
リポジトリ直下に `.env` を作成し、以下を設定してください。

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
OPENAI_API_KEY=your_openai_api_key
```

### 5. データの準備
`data/` ディレクトリを作成し、以下のファイルを配置してください：

- `data/*.py`: 解析対象のPythonスクリプトファイル（EvoShip APIの使用例など）
- `api_arg.txt` または `data/api_arg.txt`: API引数の仕様ファイル（オプション）

### 6. Neo4j の起動
Neo4j が起動済みで、URI/ユーザー/パスワードが正しいことを確認してください。

## 📖 使い方

### 1. データの取り込み

まず、`data/`ディレクトリ内のPythonスクリプトとAPI仕様ファイルを解析し、Neo4jとChromaにデータを投入します。

```bash
python ingest.py
```

このスクリプトは以下を実行します：
- `data/*.py` ファイルをTree-sitterで構文解析し、メソッド呼び出しやデータフローを抽出
- `data/api_arg.txt` からAPI引数の仕様を読み込み
- Neo4jに知識グラフを構築（既存データは削除して再構築）
- Chromaにベクトルデータベースを構築

### 2. スクリプトの生成・編集

3つのクエリスクリプトが利用可能です。それぞれ異なる検索戦略を使用します。

#### グラフ検索のみ (`query_graph.py`)

Neo4jのグラフ検索のみを使用してスクリプトを生成します。

```bash
python query_graph.py <編集対象ファイル> "<編集指示>" [オプション]
```

**例:**
```bash
python query_graph.py ./script/sample_no_bracket.py "ブラケットをつけてください。" \
  --reference ./script/samplename.py \
  -o ./script/output.py
```

#### ハイブリッド検索 (`query_hybrid.py`)

ベクトル検索（Chroma）とグラフ検索（Neo4j）を組み合わせてスクリプトを生成します。

```bash
python query_hybrid.py <編集対象ファイル> "<編集指示>" [オプション]
```

**例:**
```bash
python query_hybrid.py ./script/sample_no_bracket.py "ブラケットをつけてください。" \
  --reference ./script/samplename.py \
  -o ./script/output.py \
  --route hybrid
```

#### RAGなし (`query_norag.py`)

RAGを使わず、LLMのみでスクリプトを生成します。参考スクリプトの分析に重点を置きます。

```bash
python query_norag.py <編集対象ファイル> "<編集指示>" [オプション]
```

**例:**
```bash
python query_norag.py ./script/sample_no_bracket.py "ブラケットをつけてください。" \
  --reference ./script/samplename.py \
  -o ./script/output.py
```

#### 共通オプション

すべてのクエリスクリプトで以下のオプションが使用できます：

- `-o, --output`: 生成されたスクリプトの出力先ファイルパス
- `-r, --reference`: 参考スクリプトファイルのパス（テンプレートや例として使用）
- `--max-retries`: 最大再試行回数（デフォルト: 3）
- `--timeout-sec`: スクリプト実行のタイムアウト秒数（デフォルト: 600）
- `--keep-attempts`: 各試行のスクリプトを保存する（デフォルト: ON）
- `--no-keep-attempts`: 各試行のスクリプトを保存しない
- `--no-exec`: スクリプトを実行せず、保存のみ行う

### 3. テスト・検証

#### LLMテスト (`llm_test.py`)

APIテンプレートXMLとNeo4jデータの整合性を検証します。

```bash
python llm_test.py [オプション]
```

#### ルールテスト (`rule_test.py`)

APIルールとデータの整合性を検証します。

```bash
python rule_test.py [オプション]
```

## 📁 プロジェクト構成

### ファイル概要

#### 設定・設定ファイル

- **`config.py`**: 環境変数を読み込む設定モジュール。`.env`から`NEO4J_URI`、`NEO4J_USERNAME`、`NEO4J_PASSWORD`、`OPENAI_API_KEY`、`GEMINI_API_KEY`を取得します。

- **`requirements.txt`**: プロジェクトの依存パッケージ一覧。LangChain、Chroma、Neo4j、Tree-sitter、OpenAI関連ライブラリなどが含まれます。

- **`api_template.xml`**: EvoShip APIのテンプレート定義ファイル。

- **`.env`**: 環境変数設定ファイル（リポジトリには含まれません。各自で作成してください）。

#### データ取り込みスクリプト

- **`ingest.py`**: メインのデータ取り込みスクリプト。`data/*.py`ファイルをTree-sitterで解析し、Neo4jとChromaにデータを投入します。

#### クエリ・スクリプト生成スクリプト

- **`query_graph.py`**: グラフ検索（Neo4j）のみを使用してスクリプトを生成・編集します。
- **`query_hybrid.py`**: ベクトル検索（Chroma）とグラフ検索（Neo4j）を組み合わせたハイブリッド検索でスクリプトを生成・編集します。
- **`query_norag.py`**: RAGを使わず、LLMのみでスクリプトを生成・編集します。参考スクリプトの分析に重点を置きます。

#### テスト・検証スクリプト

- **`llm_test.py`**: APIテンプレートXMLとNeo4jデータの整合性を検証するスクリプト。
- **`rule_test.py`**: APIルールとデータの整合性を検証するスクリプト。

#### データファイル

- **`data/`**: 解析対象のPythonスクリプトファイルとAPI仕様ファイルを格納するディレクトリ
  - `data/*.py`: EvoShip APIの使用例スクリプト
  - `data/api_arg.txt`: API引数の仕様ファイル
  - `data/chroma_db/`: Chromaベクトルデータベースの永続化ディレクトリ（自動生成）

#### ドキュメント・レポート

- **`doc/`**: 過去のバージョンや実験的なスクリプト、レポートを格納
  - `doc/ingest/`: 過去の取り込みスクリプトのバージョン
  - `doc/query/`: 過去のクエリスクリプトのバージョン
  - `doc/report/`: 各種レポートファイル（Markdown形式）
  - `doc/test/`: テストスクリプトのバージョン
  - `doc/neo4j_data/`: Neo4jデータのエクスポートJSONファイル

- **`script/`**: 生成されたスクリプトやサンプルスクリプトを格納

- **`llm_report.md`**: LLMテストのレポート
- **`rule_report.md`**: ルールテストのレポート
- **`rule_api.json`**: APIルール定義ファイル

