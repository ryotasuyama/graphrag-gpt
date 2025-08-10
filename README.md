# GraphRAG Demo

このプロジェクトは、ベクトル検索とグラフ検索を組み合わせたGraphRAG（Graph Retrieval-Augmented Generation）のデモンストレーションです。文書をベクトルデータベース（Chroma）とグラフデータベース（Neo4j）の両方に保存し、質問に対して2つの異なる検索方法で回答を生成できます。

## 🚀 機能

- **ベクトル検索**: Chromaを使用したセマンティック検索
- **グラフ検索**: Neo4jを使用したグラフベース検索
- **自動文書処理**: Markdownファイルから知識グラフを自動生成
- **柔軟な検索**: 同じ質問に対して異なる検索方法を選択可能

## 📋 前提条件

- Python 3.8以上
- Neo4jデータベース（ローカルまたはクラウド）
- OpenAI APIキー

## 🛠️ セットアップ

### 1. リポジトリのクローン
```bash
git clone <repository-url>
cd graphrag_demo0624
```

### 2. 仮想環境の作成とアクティベート
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# または
venv\Scripts\activate     # Windows
```

### 3. 依存関係のインストール
```bash
pip install -r requirements.txt
```

### 4. 環境変数の設定
`.env`ファイルを作成し、以下の内容を設定してください：

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
OPENAI_API_KEY=your_openai_api_key
```

### 5. Neo4jの起動
Neo4jデータベースが起動していることを確認してください。

## 📖 使用方法

### 基本的な実行

1. **初回実行（データの取り込み）**:
```bash
python main.py
```
初回実行時は自動的に`ingest.py`が実行され、サンプルデータがベクトルDBとグラフDBに取り込まれます。

2. **質問の実行**:
```bash
# ベクトル検索を使用（デフォルト）
python query.py "スケッチ平面の作成方法を教えてください"

# グラフ検索を使用
python query.py "スケッチ平面の作成方法を教えてください" graph
```

### 個別のスクリプト実行

#### データの取り込み
```bash
python ingest.py
```
- `data/sample.md`の内容をベクトルDB（Chroma）とグラフDB（Neo4j）に取り込みます
- グラフDBは毎回初期化されてから新しいデータが挿入されます

#### 質問の実行
```bash
# ベクトル検索
python query.py "質問文" vector

# グラフ検索
python query.py "質問文" graph
```

## 📁 プロジェクト構造

```
graphrag_demo0624/
├── config.py          # 設定ファイル（環境変数管理）
├── ingest.py          # データ取り込みスクリプト
├── query.py           # 質問実行スクリプト
├── main.py            # メインランチャー
├── requirements.txt   # Python依存関係
├── data/
│   └── sample.md      # サンプルデータ
├── .chroma/           # ChromaベクトルDB（自動生成）
└── venv/              # 仮想環境
```

## 🔧 設定

### config.py
- Neo4j接続情報
- OpenAI APIキー
- 環境変数からの読み込み

### カスタマイズ可能な設定（ingest.py）
- `DOC_PATH`: 取り込む文書のパス
- `CHROMA_DIR`: ベクトルDBの保存先
- LLMモデル: 現在は`gpt-4o-mini`を使用

## 🤖 技術スタック

- **LangChain**: LLM統合とチェーン管理
- **Chroma**: ベクトルデータベース
- **Neo4j**: グラフデータベース
- **OpenAI GPT-4o-mini**: 言語モデル
- **LLMGraphTransformer**: 文書からグラフへの変換

## 🔍 検索方法の違い

### ベクトル検索（Vector）
- セマンティック類似性に基づく検索
- 文書の意味的な関連性を考慮
- 高速で柔軟な検索

### グラフ検索（Graph）
- エンティティ間の関係性を考慮した検索
- 構造化された情報の抽出
- より正確な関係性の理解

## 📝 サンプルデータ

現在のサンプルデータ（`data/sample.md`）は、Evpshipという3DCADツールのコマンドスクリプトAPI仕様書です。このデータから以下のような質問が可能です：

- "スケッチ平面の作成方法を教えてください"
- "CreateSketchPlane関数のパラメータは？"
- "スケッチ平面の軸方向はどう指定する？"

## 🚨 トラブルシューティング

### Neo4j接続エラー
```
RuntimeError: Neo4j に接続できません。起動を確認してください
```
- Neo4jデータベースが起動していることを確認
- 接続情報（URI、ユーザー名、パスワード）が正しいことを確認

### OpenAI APIエラー
- APIキーが正しく設定されていることを確認
- APIクォータが残っていることを確認

### 依存関係エラー
```bash
pip install -r requirements.txt --upgrade
```

## 📄 ライセンス

このプロジェクトはデモンストレーション目的で作成されています。

## 🤝 貢献

バグ報告や機能要望は、GitHubのIssueでお知らせください。 