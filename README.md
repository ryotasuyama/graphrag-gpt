# GraphRAG GPT

このプロジェクトは、ベクトル検索（Chroma）とグラフ検索（Neo4j）を組み合わせた GraphRAG（Graph Retrieval-Augmented Generation）の実装です。Pythonスクリプトファイル（`data/*.py`）をソースとして、Tree-sitterによる構文解析で知識グラフを構築し、CADアプリケーション「EvoShip」のAPI操作コードを生成・編集できます。

## 🚀 特徴

- ベクトル検索: Chroma + OpenAI Embeddings によるセマンティック検索
- グラフ検索: Neo4j + Cypher 生成チェーンによるグラフQA
- Tree-sitterベースの取り込み: Pythonスクリプトを構文解析し、メソッド呼び出しやデータフローを抽出してグラフを構築
- スクリプト編集機能: 既存のPythonスクリプトを編集指示に基づいて自動修正・生成
- 冪等な再構築: 取り込み時にNeo4jを初期化して再構築（実行毎に同じ結果）

## 📋 前提条件

- Python 3.10以上
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

### 取り込み（ingest）

```bash
python ingest1025.py
```

- `data/` 配下の `*.py` ファイルを読み込み、Tree-sitterで構文解析します。
- メソッド呼び出し、データフロー、変数の依存関係を抽出してグラフを構築します。
- 抽出した情報をChroma（ベクトルDB）とNeo4j（グラフDB）に登録します。
- 実行時、Neo4j 上の既存ノード/リレーションは削除されます（`MATCH (n) DETACH DELETE n`）。

### スクリプト生成・編集（query）

```bash
# 既存スクリプトの編集
python query1228.py <ファイルパス> "<編集指示>" -o <出力先>

# 例: ブラケットを追加
python query1228.py ./script/sample.py "ブラケットをつけてください。" -o ./script/output.py

# 参考スクリプトを指定して編集
python query1228.py ./script/sample.py "ブラケットをつけてください。" --reference ./script/reference.py -o ./script/output.py

# スクリプトを実行せずに保存のみ（デバッグ用）
python query1228.py <ファイルパス> "<編集指示>" --no-exec -o <出力先>
```

主なオプション:

- `-o, --output`: 生成されたスクリプトの出力先ファイルパス
- `-r, --reference`: 参考スクリプトファイルのパス（テンプレートとして使用）
- `--max-retries`: 最大再試行回数（デフォルト: 3）
- `--timeout-sec`: スクリプト実行のタイムアウト秒数（デフォルト: 60）
- `--no-exec`: スクリプトを実行せず、保存のみ行う
- `--no-keep-attempts`: 各試行のスクリプトを保存しない（デフォルトは保存）

**注意**: `query1228.py` はグラフ検索のみを使用します。ベクトル検索とグラフ検索の両方を利用して、既存スクリプトの編集指示に基づいたコード生成を行います。

## 📁 プロジェクト構成

```
graphrag-gpt/
├── config.py           # 環境変数読み込み
├── ingest1025.py       # 取り込み: Pythonスクリプト解析, Chroma登録, Neo4j再構築
├── query1228.py       # スクリプト生成・編集: 既存スクリプトの編集機能付き
├── requirements.txt   # 依存関係
├── data/              # データディレクトリ
│   ├── *.py           # 解析対象のPythonスクリプトファイル
│   ├── api_arg.txt    # API引数仕様ファイル（オプション）
│   └── chroma_db/     # ChromaベクトルDBの保存先（自動生成）
├── script/            # 生成・編集されたスクリプトの保存先
├── doc/               # 過去の実装やレポート（参考資料）
└── venv/              # 仮想環境（任意）
```

## 🔧 設定の要点

- `config.py`: `.env` を読み込んで `NEO4J_*` と `OPENAI_API_KEY` を使用します。
- `ingest1025.py`: 
  - Chroma の保存先は `data/chroma_db`（自動生成）
  - Tree-sitterでPythonスクリプトを構文解析し、メソッド呼び出しとデータフローを抽出
  - Neo4j を毎回初期化して再構築します
- `query1228.py`: 
  - グラフ検索のみを使用（ベクトル検索も内部的に利用）
  - デフォルトモデルは `gpt-5.2`（`config.py`で変更可能）
  - 生成されたスクリプトは自動実行され、エラー時は再試行されます

## 🔍 技術的な詳細

### 取り込みプロセス（ingest1025.py）

1. **スクリプト解析**: Tree-sitterを使用してPythonスクリプトを構文解析
2. **グラフ抽出**: 
   - メソッド呼び出し（`MethodCall`ノード）
   - スクリプト例（`ScriptExample`ノード）
   - データフロー（`USES`リレーション）
   - メソッド間の関係（`IS_EXAMPLE_OF`リレーション）
3. **データベース登録**:
   - Neo4j: グラフ構造として保存
   - Chroma: テキスト埋め込みとして保存

### クエリプロセス（query1228.py）

1. **コンテキスト取得**: グラフ検索とベクトル検索の両方を使用
2. **コード生成**: LLM（GPT-5.2）を使用して編集指示に基づきコードを生成
3. **実行検証**: 生成されたスクリプトを実行し、エラー時は再試行

## 📝 データについて

- `data/*.py`: EvoShip APIの使用例を含むPythonスクリプトファイル
- `doc/`: 過去の実装履歴やレポート（2025年の開発資料を含む）

## 🚨 トラブルシューティング

### Neo4j 接続エラー
- Neo4j が起動しているか、`NEO4J_URI/USERNAME/PASSWORD` が正しいか確認
- 例外: `RuntimeError: Neo4j に接続できません。起動を確認してください`

### OpenAI API エラー
- `OPENAI_API_KEY` の設定、利用上限を確認
- モデル名（`gpt-5.2`）が利用可能か確認

### データファイルが見つからない
- `data/` ディレクトリが存在し、`*.py` ファイルが含まれているか確認
- `api_arg.txt` が必要な場合は、プロジェクトルートまたは `data/` に配置

### 依存関係エラー
```bash
pip install -r requirements.txt --upgrade
```

### Tree-sitter のエラー
```bash
pip install tree-sitter tree-sitter-python --upgrade
```

### スクリプト実行エラー（query1228.py）
- 生成されたスクリプトに構文エラーがないか確認
- `--no-exec` オプションで実行をスキップしてデバッグ
- `--keep-attempts` オプションで各試行のスクリプトを確認

## 📚 参考資料

- `doc/` ディレクトリに2025年の開発履歴やレポートが含まれています
- 過去の実装例は `doc/ingest/` と `doc/query/` を参照してください

## 📄 ライセンス / 🤝 貢献

デモ用途のサンプルです。バグ報告や要望は Issue でお知らせください。