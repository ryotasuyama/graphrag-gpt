from pathlib import Path
import re
import json
from typing import List, Dict, Any, Tuple
import shutil

import config
from langchain_core.documents import Document
from langchain_neo4j import Neo4jGraph
from neo4j.exceptions import ServiceUnavailable
from langchain_community.graphs.graph_document import GraphDocument, Node, Relationship
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings ,ChatOpenAI

DATA_DIR = Path("data")
HELP_DIR = Path("help")
BRACKET_TYPE_REF_PATH = Path("prompts/bracket_type_reference.md")
NEO4J_URI = config.NEO4J_URI
NEO4J_USER = config.NEO4J_USER
NEO4J_PASSWORD = config.NEO4J_PASSWORD
NEO4J_DATABASE = getattr(config, "NEO4J_DATABASE", "neo4j")

# api.txt 関連の定義を削除 (API_TXT_CANDIDATES)

API_ARG_TXT_CANDIDATES = [
    Path("/mnt/data/api_arg.txt"),
    Path("api_arg.txt"),
    DATA_DIR / "api_arg.txt",
]

CHROMA_PERSIST_DIR = DATA_DIR / "chroma_db"
OPENAI_API_KEY = config.OPENAI_API_KEY

llm = ChatOpenAI(
    temperature=0,
    model_name="gpt-5.2",
    openai_api_key=OPENAI_API_KEY,
    # request_timeout=600
)

def _read_api_arg_text() -> str:
    """api_arg.txt を候補パスから読み込む"""
    for p in API_ARG_TXT_CANDIDATES:
        if p.exists():
            return p.read_text(encoding="utf-8")
    raise FileNotFoundError("api_arg.txt が見つかりませんでした。")

def _extract_graph_from_specs_with_llm(raw_text: str) -> Dict[str, List[Dict[str, Any]]]:
    """LLMを使ってAPI仕様書の生テキストからノードとリレーションを抽出する"""
    prompt = f"""
        あなたはAPI仕様書を解析し、知識グラフを構築する専門家です。
        以下のAPI仕様書テキストから、指定されたスキーマに従ってノードとリレーションを抽出し、JSON形式で出力してください。

        --- グラフのスキーマ定義 ---
        1.  **ノードの種類とプロパティ:**
            - `Object`: APIの操作対象となるオブジェクト。 (例: "Part")
                - `id`: オブジェクト名 (例: "Part")
                - `properties`: {{ "name": "オブジェクト名" }}
            - `Method`: オブジェクトに属するメソッド。
                - `id`: メソッド名 (例: "CreateVariable")
                - `properties`: {{ "name": "メソッド名", "description": "メソッドの日本語説明" }}
            - `Parameter`: メソッドが受け取る引数。
                - `id`: `メソッド名_引数名` (例: "CreateVariable_VariableName")
                - `properties`: {{ "name": "引数名", "description": "引数の説明", "order": 引数の順番(0から) }}
            - `ReturnValue`: メソッドの戻り値。
                - `id`: `メソッド名_ReturnValue` (例: "CreateVariable_ReturnValue")
                - `properties`: {{ "description": "戻り値の説明" }}
            - `DataType`: 引数や戻り値、属性の型。
                - `id`: データ型名 (例: "文字列", "長さ", "bool", "ブラケット要素のパラメータオブジェクト", "整数")
                - `properties`: {{ "name": "データ型名" }} # 説明は後で別のプロンプトで付与します
            - `Attribute`: パラメータオブジェクトが持つ属性。
                - `id`: `データ型名_属性名` (例: "ブラケット要素のパラメータオブジェクト_DefinitionType")
                - `properties`: {{ "name": "属性名", "description": "属性の日本語説明 (型情報を除いたもの)" }}

        2.  **リレーションの種類:**
            - `BELONGS_TO`: (Method) -> (Object)
            - `HAS_PARAMETER`: (Method) -> (Parameter)
            - `HAS_RETURNS`: (Method) -> (ReturnValue)
            - `HAS_TYPE`: (Parameter) -> (DataType), (ReturnValue) -> (DataType), (Attribute) -> (DataType)
            - `HAS_ATTRIBUTE`: (DataType) -> (Attribute)

        --- 抽出ルール ---
        1.  `■オブジェクト名` は `Object` ノードとし、後続の `Method` は `BELONGS_TO` で接続してください。
        2.  `〇〇パラメータオブジェクト` というセクションは `DataType` ノードとしてください。
        3.  上記 `DataType` に続く `属性` (例: `DefinitionType //s整数: ...`) は `Attribute` ノード (`id: DataType_Attr`) とし、`DataType` に `HAS_ATTRIBUTE` で接続してください。
        4.  `Attribute` の `description` には型情報 (例: `整数:`, `文字列：`) を *除いた* 説明文 (例: "ブラケットの作成方法指定...") を格納してください。
        5.  `//` の後の説明文に型情報 (例: `整数:`) が含まれる場合、(Attribute)から該当`DataType` (例: "整数") へ `HAS_TYPE` リレーションを張ってください。
        6.  `Create[... ]Param` (例: `CreateBracketParam`) メソッドは、対応する `〇〇パラメータオブジェクト` (例: "ブラケット要素のパラメータオブジェクト") を `DataType` とする `ReturnValue` を持つ `Method` として抽出してください。
        7.  Parameterノードのdescriptionには、`：`の後の文章をそのまま指定してください。

        --- 出力形式 ---
        - 全体を1つのJSONオブジェクトで出力してください。
        - **`nodes`** の値は、以下の形式の**ノードオブジェクト**のリストです:
        `{{"id": "一意のID", "type": "ノードの種類", "properties": {{...}} }}`
        - **`relationships`** の値は、以下の形式の**リレーションオブジェクト**のリストです:
        `{{"source": "ソースノードID", "target": "ターゲットノードID", "type": "リレーションの種類"}}`

        --- API仕様書テキスト ---
        {raw_text}
        --- ここまで ---

        抽出後のJSON:
    """
    try:
        response = llm.invoke(prompt)
        # マークダウンのコードブロックからJSON部分を抽出
        match = re.search(r"```json\s*([\s\S]+?)\s*```", response.content)
        if match:
            json_str = match.group(1)
            return json.loads(json_str)
        else:
            # コードブロックがない場合、直接パースを試みる
            return json.loads(response.content)
    except Exception as e:
        print(f"      ⚠ LLMによるグラフ抽出またはJSONパース中にエラー: {e}")
        return {"nodes": [], "relationships": []}

def _extract_datatype_descriptions_with_llm(raw_text: str) -> Dict[str, str]:
    """LLMを使ってapi_arg.txtからデータ型の説明を抽出し、辞書形式で返す"""
    prompt = f"""
    あなたはAPI仕様書のデータ型定義を解析する専門家です。
    以下のテキストから、データ型とその説明文を抽出し、JSON形式で出力してください。

    --- 解析ルール ---
    1.  `■` (U+25A0) で始まる行は、新しいデータ型の定義開始を示します。
    2.  `■` の後に続くテキストが「データ型名」です (例: `■文字列` -> "文字列")。
    3.  データ型名の次の行から、次の `■` が出現する直前まで、またはファイルの終わりまでが、そのデータ型の「説明文」です。
    4.  説明文は、改行を含めてそのまま連結してください。

    --- 出力形式 ---
    - 全体を1つのJSONオブジェクトで出力してください。
    - キーを「データ型名」、値を「説明文」とした辞書(マップ)形式とします。
    - 例: {{"文字列": "通常の文字列", "浮動小数点": "通常の数値\n\n例: 3.14"}}
    - JSONはマークダウンのコードブロック(` ```json ... ``` `)で囲んでください。
    - JSONオブジェクトにはコメントをいれないでください。
    - 必ずJSONオブジェクトで出力してください。

    --- データ型定義テキスト ---
    {raw_text}
    --- ここまで ---

    抽出後のJSON:
    """
    try:
        response = llm.invoke(prompt)
        # マークダウンのコードブロックからJSON部分を抽出
        match = re.search(r"```json\s*([\s\S]+?)\s*```", response.content)
        if match:
            json_str = match.group(1)
            return json.loads(json_str)
        else:
            # コードブロックがない場合、直接パースを試みる
            return json.loads(response.content)
    except Exception as e:
        print(f"      ⚠ LLMによるデータ型説明の抽出またはJSONパース中にエラー: {e}")
        return {}

def extract_triples_from_specs(
    graph_data: Dict[str, List[Dict[str, Any]]],
    type_descriptions: Dict[str, str]
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    """LLMが抽出したグラフデータから、後続処理で利用するトリプル形式を生成する"""

    triples: List[Dict[str, Any]] = []
    node_props: Dict[str, Dict[str, Any]] = {}

    nodes = graph_data.get("nodes", [])
    relationships = graph_data.get("relationships", [])

    node_type_map = {}

    # 1. ノード情報を node_props と node_type_map に格納
    for node in nodes:
        node_id = node["id"]
        node_type = node["type"]
        properties = node.get("properties", {})

        # DataTypeノードへの説明追加は呼び出し元で行う
        # if node_type == "DataType" and properties.get("name") in type_descriptions:
        #     properties["description"] = type_descriptions[properties["name"]]

        node_props[node_id] = {"type": node_type, "properties": properties}
        node_type_map[node_id] = node_type

    # 2. リレーション情報からトリプルを生成
    for rel in relationships:
        source_id = rel["source"]
        target_id = rel["target"]

        # マップに存在しないノードIDの場合はスキップ
        if source_id not in node_type_map or target_id not in node_type_map:
            continue

        triples.append({
            "source": source_id,
            "source_type": node_type_map[source_id],
            "label": rel["type"],
            "target": target_id,
            "target_type": node_type_map[target_id],
        })

    return triples, node_props


def _triples_to_graph_documents(triples: List[Dict[str, Any]], node_props: Dict[str, Dict[str, Any]]) -> List[GraphDocument]:
    node_map: Dict[str, Node] = {}
    for node_id, meta in node_props.items():
        if node_id in node_map:
            existing_node = node_map[node_id]
            existing_node.properties.update(meta.get("properties", {}))
        else:
            ntype = meta["type"]
            props = meta.get("properties", {})
            node_map[node_id] = Node(id=node_id, type=ntype, properties=props)

    rels: List[Relationship] = []
    for t in triples:
        source_node = node_map.get(t["source"])
        if not source_node:
            source_node = Node(id=t["source"], type=t["source_type"])
            node_map[t["source"]] = source_node

        target_node = node_map.get(t["target"])
        if not target_node:
            target_node = Node(id=t["target"], type=t["target_type"])
            node_map[t["target"]] = target_node

        rels.append(
            Relationship(
                source=source_node,
                target=target_node,
                type=t["label"],
                properties={}
            )
        )

    doc = Document(page_content="API Spec and Example graph")
    gdoc = GraphDocument(nodes=list(node_map.values()), relationships=rels, source=doc)
    return [gdoc]

def _rebuild_graph_in_neo4j(graph_docs: List[GraphDocument]) -> Tuple[int, int]:
    graph = Neo4jGraph(
        url=NEO4J_URI,
        username=NEO4J_USER,
        password=NEO4J_PASSWORD,
        database=NEO4J_DATABASE,
    )

    print("🧹 Neo4jの既存データを削除中...")
    delete_query = "MATCH (n) DETACH DELETE n"
    graph.query(delete_query)

    print(f"\n🚀 Neo4jにデータを投入中...")

    graph.add_graph_documents(graph_docs)

    res_nodes = graph.query("MATCH (n) RETURN count(n) AS c")
    res_rels = graph.query("MATCH ()-[r]->() RETURN count(r) AS c")
    return int(res_nodes[0]["c"]), int(res_rels[0]["c"])

def _build_and_load_chroma(
    triples: List[Dict[str, Any]],
    node_props: Dict[str, Dict[str, Any]]
    ) -> None:
    """
    triples (リレーション定義) と node_props (ノード定義) を受け取り、
    それらをそのままベクトル化してChromaDBに保存する。
    """
    print("\n🚀 ChromaDBのベクトルデータを生成・保存中...")

    if CHROMA_PERSIST_DIR.exists():
        shutil.rmtree(CHROMA_PERSIST_DIR)
    CHROMA_PERSIST_DIR.mkdir(exist_ok=True)

    docs_for_vectorstore: List[Document] = []

    if not node_props and not triples:
        print("⚠ データ(node_props/triples)が見つからないため、ChromaDBの構築をスキップします。")
        return

    # 1. ノードのベクトル化
    # node_props = { "NodeID": { "type": "Type", "properties": {...} }, ... }
    print(f"✔ {len(node_props)} 個のノード定義をベクトル化の対象とします。")
    for node_id, meta in node_props.items():
        node_type = meta.get("type", "Unknown")
        properties = meta.get("properties", {})

        # ノード情報を文字列化
        content = f"Node ID: {node_id}\nNode Type: {node_type}\nProperties: {json.dumps(properties, ensure_ascii=False)}"

        metadata = {
            "source": "graph_node",
            "node_id": node_id,
            "node_type": node_type,
        }
        docs_for_vectorstore.append(Document(page_content=content, metadata=metadata))

    # 2. リレーションのベクトル化
    # triples = [ {"source": "ID", "source_type": "Type", "label": "REL", "target": "ID", "target_type": "Type"}, ... ]
    print(f"✔ {len(triples)} 個のリレーション定義をベクトル化の対象とします。")
    for rel in triples:
        source_id = rel.get("source")
        target_id = rel.get("target")
        rel_type = rel.get("label")

        # リレーションを表すテキストを作成
        content = f"Relationship: {source_id} -[{rel_type}]-> {target_id}"

        metadata = {
            "source": "graph_relationship",
            "source_node": source_id,
            "target_node": target_id,
            "relation_type": rel_type,
        }
        docs_for_vectorstore.append(Document(page_content=content, metadata=metadata))

    # ChromaDBに投入する前のデータをJSONファイルとして保存
    chroma_data_to_save = [
        {"page_content": doc.page_content, "metadata": doc.metadata}
        for doc in docs_for_vectorstore
    ]
    with open("chroma_data.json", "w", encoding="utf-8") as f:
        json.dump(chroma_data_to_save, f, indent=2, ensure_ascii=False)
    print("💾 ChromaDB投入前のデータを 'chroma_data.json' に保存しました。")

    try:
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        vectorstore = Chroma.from_documents(
            documents=docs_for_vectorstore,
            embedding=embeddings,
            persist_directory=str(CHROMA_PERSIST_DIR),
        )
        print(f"✔ Chroma DB created and persisted with {len(docs_for_vectorstore)} documents at: {CHROMA_PERSIST_DIR}")
    except Exception as e:
        print(f"⚠ Chroma DBの作成に失敗しました: {e}")


# ============================================================
# Help HTML / BracketType 統合 (PLAN_help_neo4j_integration.md)
# ============================================================

def _parse_help_directory(help_dir: Path) -> List[Dict[str, Any]]:
    """
    Help HTMLディレクトリを解析してページ情報のリストを返す。LLM不使用。
    - Tier1 (cmd_): soup.get_text() でプレーンテキスト抽出、機械的にsummary/keywords生成
    - Tier2 (about_, sample_): html2text でMarkdown変換（LLMに渡すため）
    """
    try:
        from bs4 import BeautifulSoup
        import html2text as html2text_lib
    except ImportError as e:
        print(f"⚠ 必要なライブラリがインストールされていません: {e}")
        print("  pip install beautifulsoup4 html2text を実行してください。")
        return []

    if not help_dir.exists():
        print(f"⚠ Help ディレクトリが見つかりません: {help_dir}")
        return []

    h2t = html2text_lib.HTML2Text()
    h2t.ignore_links = True
    h2t.ignore_images = True
    h2t.body_width = 0  # 折り返しなし

    pages = []
    html_files = sorted(help_dir.glob("*.html"))
    print(f"  {len(html_files)} 個のHTMLファイルを検出しました。")

    for html_file in html_files:
        file_name = html_file.stem  # e.g., "cmd_ship_bracket"

        # page_type の判定
        if file_name.startswith("cmd_"):
            page_type = "cmd"
        elif file_name.startswith("about_"):
            page_type = "about"
        elif file_name.startswith("sample_"):
            page_type = "sample"
        else:
            page_type = "other"

        try:
            html_content = html_file.read_text(encoding="utf-8")
            soup = BeautifulSoup(html_content, "html.parser")

            # タイトル抽出
            title_tag = soup.find("title")
            title = title_tag.get_text(strip=True) if title_tag else file_name

            # href リンク抽出（同一ディレクトリの .html ファイルのみ）
            hrefs = []
            seen_hrefs = set()
            for a_tag in soup.find_all("a", href=True):
                href = a_tag["href"]
                if href.endswith(".html") and not href.startswith("http"):
                    linked_stem = Path(href).stem
                    if linked_stem not in seen_hrefs and linked_stem != file_name:
                        hrefs.append(linked_stem)
                        seen_hrefs.add(linked_stem)

            if page_type == "cmd":
                # Tier1: soup.get_text() のみ、LLM不使用
                raw_text = soup.get_text(separator="\n", strip=True)

                # summary: 最初の意味のある段落テキスト
                summary = title
                for tag in soup.find_all(["p", "li"]):
                    text = tag.get_text(strip=True)
                    if text and len(text) > 10:
                        summary = text[:200]
                        break

                # keywords: ファイル名パーツ + タイトル単語
                name_parts = file_name.replace("cmd_", "").split("_")
                title_words = [w for w in title.split() if len(w) > 1]
                keywords = list(dict.fromkeys(name_parts + title_words[:5]))
                keywords = [kw for kw in keywords if kw]

            else:
                # Tier2 (about_, sample_, other): html2text でMarkdown変換
                raw_text = h2t.handle(html_content)

                # 暫定 summary/keywords（LLM で後から上書き）
                summary = title
                name_parts = (
                    file_name.replace("about_", "")
                    .replace("sample_", "")
                    .split("_")
                )
                title_words = [w for w in title.split() if len(w) > 1]
                keywords = list(dict.fromkeys(name_parts + title_words[:5]))
                keywords = [kw for kw in keywords if kw]

            pages.append({
                "id": file_name,
                "file_name": file_name,
                "title": title,
                "page_type": page_type,
                "summary": summary,
                "keywords": keywords,
                "raw_text": raw_text[:3000],  # Neo4j格納用に上限設定
                "hrefs": hrefs,               # リレーション生成用（Neo4jには格納しない）
            })

        except Exception as e:
            print(f"  ⚠ {html_file.name} の解析中にエラー: {e}")

    tier_counts = {}
    for p in pages:
        tier_counts[p["page_type"]] = tier_counts.get(p["page_type"], 0) + 1
    print(f"  解析完了: " + ", ".join(f"{k}={v}" for k, v in sorted(tier_counts.items())))
    return pages


def _parse_bracket_type_reference(
    md_path: Path,
) -> Tuple[List[Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    """
    prompts/bracket_type_reference.md をパースして BracketShapeType / DimensionType
    のノードを返す。正規表現のみ使用、LLM不使用。

    Returns:
        triples: リレーション（現時点では空、DEFINES は _help_pages_to_triples() で生成）
        node_props: { node_id: { type, properties } }
    """
    if not md_path.exists():
        print(f"⚠ {md_path} が見つかりません。スキップします。")
        return [], {}

    content = md_path.read_text(encoding="utf-8")
    triples: List[Dict[str, Any]] = []
    node_props: Dict[str, Dict[str, Any]] = {}

    # Markdown テーブル行のパターン: | **1501** | 2-B | ... | ... |
    table_row_pattern = re.compile(
        r"^\|\s*\*{0,2}(-?\d+)\*{0,2}\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|"
    )

    # --- BracketShapeType の解析 ---
    # (?=\n### [^#]|\Z): "### " で始まる次のセクション直前まで（"####" は除外）
    bracket_section_match = re.search(
        r"### BracketType.*?(?=\n### [^#]|\Z)", content, re.DOTALL
    )
    if bracket_section_match:
        bracket_section = bracket_section_match.group(0)
        current_category = "other"

        for line in bracket_section.splitlines():
            if "2面" in line:
                current_category = "2面"
            elif "3面" in line:
                current_category = "3面"

            m = table_row_pattern.match(line.strip())
            if not m:
                continue

            bracket_type = int(m.group(1))
            shape_name = m.group(2).strip()
            params_raw = m.group(3).strip()
            usage_note = m.group(4).strip()

            # パラメータリスト抽出: `[D, R]` -> ["D", "R"]
            params_match = re.search(r"\[([^\]]*)\]", params_raw)
            if params_match:
                bracket_params = [
                    p.strip()
                    for p in params_match.group(1).split(",")
                    if p.strip()
                ]
            else:
                bracket_params = []

            node_id = f"BracketShapeType_{bracket_type}"
            node_props[node_id] = {
                "type": "BracketShapeType",
                "properties": {
                    "id": node_id,
                    "bracket_type": bracket_type,
                    "shape_name": shape_name,
                    "bracket_params": bracket_params,
                    "category": current_category,
                    "usage_note": usage_note,
                },
            }

    # --- DimensionType の解析 ---
    dim_section_match = re.search(
        r"### Sf1/Sf2 DimensionType.*?(?=\n### [^#]|\Z)", content, re.DOTALL
    )
    if dim_section_match:
        dim_section = dim_section_match.group(0)

        for line in dim_section.splitlines():
            m = table_row_pattern.match(line.strip())
            if not m:
                continue

            dim_type = int(m.group(1))
            shape_name = m.group(2).strip()
            params_raw = m.group(3).strip()
            usage_note = m.group(4).strip()

            params_match = re.search(r"\[([^\]]*)\]", params_raw)
            if params_match:
                params = [
                    p.strip()
                    for p in params_match.group(1).split(",")
                    if p.strip()
                ]
            else:
                params = []

            node_id = f"DimensionType_{dim_type}"
            node_props[node_id] = {
                "type": "DimensionType",
                "properties": {
                    "id": node_id,
                    "dim_type": dim_type,
                    "shape_name": shape_name,
                    "params": params,
                    "usage_note": usage_note,
                },
            }

    bracket_count = sum(1 for v in node_props.values() if v["type"] == "BracketShapeType")
    dim_count = sum(1 for v in node_props.values() if v["type"] == "DimensionType")
    print(f"  BracketShapeType: {bracket_count} 件, DimensionType: {dim_count} 件")
    return triples, node_props


def _extract_help_summaries_with_llm(
    pages: List[Dict[str, Any]],
    existing_method_names: List[str],
    existing_object_names: List[str],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Tier2ページ（about_, sample_）に対してLLMでsummary/keywordsと
    DESCRIBES リレーションを抽出する。8ページごとにバッチ処理。

    Returns:
        pages: summaryとkeywordsが更新されたページリスト
        llm_rels: LLMが生成したDESCRIBESトリプルのリスト
    """
    tier2_pages = [p for p in pages if p["page_type"] in ("about", "sample")]
    if not tier2_pages:
        return pages, []

    print(f"  Tier2対象: {len(tier2_pages)} ページ")
    all_llm_rels: List[Dict[str, Any]] = []

    # 既存APIノード名のセット（検証用）
    method_set = set(existing_method_names)
    object_set = set(existing_object_names)

    # LLMに渡すAPIノード名リスト（長すぎる場合はカット）
    methods_list = ", ".join(existing_method_names[:80])
    objects_list = ", ".join(existing_object_names[:30])

    BATCH_SIZE = 8
    total_batches = (len(tier2_pages) + BATCH_SIZE - 1) // BATCH_SIZE

    page_by_filename = {p["file_name"]: p for p in pages}

    for batch_idx in range(0, len(tier2_pages), BATCH_SIZE):
        batch = tier2_pages[batch_idx : batch_idx + BATCH_SIZE]
        batch_num = batch_idx // BATCH_SIZE + 1

        # バッチテキスト構築（各ページ最大1500文字）
        pages_text = ""
        for page in batch:
            pages_text += (
                f"\n### ページ: {page['file_name']}\n"
                f"タイトル: {page['title']}\n\n"
                f"{page['raw_text'][:1500]}\n"
            )

        prompt = f"""以下のヘルプページの内容を解析し、JSONでデータを出力してください。

【既存 API ノード名（DESCRIBESのターゲットとして使用可能なもののみ）】
Method: {methods_list}
Object: {objects_list}

【出力形式】
```json
{{
  "pages": [
    {{
      "file_name": "ファイル名（拡張子なし）",
      "summary": "このページの内容を1〜2文で要約",
      "keywords": ["キーワード1", "キーワード2"],
      "describes": ["MethodName1", "ObjectName1"]
    }}
  ]
}}
```
※ describes には上記の既存APIノード名のみ記載してください。該当なければ空リストにしてください。

【ページ一覧】
{pages_text}

JSONを ```json ... ``` で囲んで出力:"""

        try:
            response = llm.invoke(prompt)
            match = re.search(r"```json\s*([\s\S]+?)\s*```", response.content)
            if match:
                result = json.loads(match.group(1))
            else:
                result = json.loads(response.content)

            for page_result in result.get("pages", []):
                fn = page_result.get("file_name")
                if not fn or fn not in page_by_filename:
                    continue

                page = page_by_filename[fn]
                if page_result.get("summary"):
                    page["summary"] = page_result["summary"]
                if page_result.get("keywords"):
                    page["keywords"] = page_result["keywords"]

                # DESCRIBES リレーション（既存ノードに限定）
                for target_name in page_result.get("describes", []):
                    if target_name in method_set:
                        all_llm_rels.append({
                            "source": fn, "source_type": "HelpPage",
                            "label": "DESCRIBES",
                            "target": target_name, "target_type": "Method",
                        })
                    elif target_name in object_set:
                        all_llm_rels.append({
                            "source": fn, "source_type": "HelpPage",
                            "label": "DESCRIBES",
                            "target": target_name, "target_type": "Object",
                        })

            print(f"  ✔ Tier2バッチ {batch_num}/{total_batches} 完了 ({len(batch)} ページ)")

        except Exception as e:
            print(f"  ⚠ Tier2バッチ {batch_num} のLLM処理エラー: {e}")

    return pages, all_llm_rels


def _help_pages_to_triples(
    pages: List[Dict[str, Any]],
    llm_rels: List[Dict[str, Any]],
    bracket_node_props: Dict[str, Dict[str, Any]],
    existing_method_names: List[str],
    existing_object_names: List[str],
) -> Tuple[List[Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    """
    HelpPageノードとリレーション（RELATED_TO, DESCRIBES, DEFINES）を
    トリプル形式に変換する。

    - RELATED_TO: HTML内のhrefから決定論的に生成
    - DESCRIBES (cmd_): ファイル名パーツとAPIノード名のマッチング（Technique A）
    - DESCRIBES (about_): LLMが生成したllm_relsを使用（Technique C）
    - DEFINES: cmd_ship_bracket → BracketShapeType
    """
    triples: List[Dict[str, Any]] = []
    node_props: Dict[str, Dict[str, Any]] = {}

    # --- HelpPage ノード生成 ---
    page_ids = set(p["id"] for p in pages)
    for page in pages:
        node_id = page["id"]
        node_props[node_id] = {
            "type": "HelpPage",
            "properties": {
                "id": node_id,
                "file_name": page["file_name"],
                "title": page["title"],
                "page_type": page["page_type"],
                "summary": page.get("summary", ""),
                "keywords": page.get("keywords", []),
                "raw_text": page.get("raw_text", "")[:2000],
                "source": "help",
            },
        }

    # --- RELATED_TO リレーション（href から）---
    seen_rels: set = set()

    def _add_triple(t: Dict[str, Any]) -> None:
        key = (t["source"], t["label"], t["target"])
        if key not in seen_rels:
            seen_rels.add(key)
            triples.append(t)

    for page in pages:
        for href_stem in page.get("hrefs", []):
            if href_stem in page_ids:
                _add_triple({
                    "source": page["id"], "source_type": "HelpPage",
                    "label": "RELATED_TO",
                    "target": href_stem, "target_type": "HelpPage",
                })

    # --- DESCRIBES リレーション（Technique A: cmd_ ページのファイル名マッチング）---
    method_name_lower = {m.lower(): m for m in existing_method_names}
    object_name_lower = {o.lower(): o for o in existing_object_names}

    for page in pages:
        if page["page_type"] != "cmd":
            continue
        # "cmd_ship_bracket" -> ["ship", "bracket"]
        parts = page["file_name"].replace("cmd_", "").split("_")

        for part in parts:
            if len(part) < 3:
                continue
            part_lower = part.lower()

            for method_lower, method_name in method_name_lower.items():
                if part_lower in method_lower:
                    _add_triple({
                        "source": page["id"], "source_type": "HelpPage",
                        "label": "DESCRIBES",
                        "target": method_name, "target_type": "Method",
                    })

            for obj_lower, obj_name in object_name_lower.items():
                if part_lower in obj_lower:
                    _add_triple({
                        "source": page["id"], "source_type": "HelpPage",
                        "label": "DESCRIBES",
                        "target": obj_name, "target_type": "Object",
                    })

    # --- DESCRIBES リレーション（Technique C: LLM生成、about_ ページ）---
    for rel in llm_rels:
        _add_triple(rel)

    # --- BracketShapeType / DimensionType ノードを追加 ---
    node_props.update(bracket_node_props)

    # --- DEFINES リレーション（cmd_ship_bracket → BracketShapeType）---
    bracket_page_id = "cmd_ship_bracket"
    if bracket_page_id in node_props:
        for node_id, meta in bracket_node_props.items():
            if meta["type"] == "BracketShapeType":
                _add_triple({
                    "source": bracket_page_id, "source_type": "HelpPage",
                    "label": "DEFINES",
                    "target": node_id, "target_type": "BracketShapeType",
                })

    describes_count = sum(1 for t in triples if t["label"] == "DESCRIBES")
    related_count = sum(1 for t in triples if t["label"] == "RELATED_TO")
    defines_count = sum(1 for t in triples if t["label"] == "DEFINES")
    print(
        f"  HelpPage: {len(pages)} ノード, "
        f"DESCRIBES: {describes_count}, RELATED_TO: {related_count}, DEFINES: {defines_count}"
    )
    return triples, node_props


def _build_and_load_neo4j() -> Tuple[List[GraphDocument], List[Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    """
    API仕様とスクリプト例を解析し、Neo4jにグラフを構築する。
    その後、Help HTML と BracketShapeType/DimensionType を MERGE で追加する。

    Returns:
        Tuple containing:
        1. gdocs (Neo4j挿入用)
        2. all_triples (ChromaDB挿入用の生リレーションデータ)
        3. all_node_props (ChromaDB挿入用の生ノードデータ)
    """
    # --- 1. API仕様書 (api*.txt, api_arg.txt) の解析 ---
    print("📄 API仕様書を解析中...")

    # 4つのAPI仕様書ファイルを定義
    api_txt_files = [
        DATA_DIR / "api1.txt",
        DATA_DIR / "api2.txt",
        DATA_DIR / "api3.txt",
        DATA_DIR / "api4.txt",
        DATA_DIR / "api5.txt",
    ]

    all_nodes = []
    all_relationships = []

    # LLMでAPI仕様書から直接グラフ構造(ノード/リレーション)を抽出
    print("🤖 LLMによるAPI仕様書からのグラフ抽出を実行中...")

    for api_file_path in api_txt_files:
        if not api_file_path.exists():
            print(f"⚠ 警告: {api_file_path} が見つかりません。スキップします。")
            continue

        print(f"  - ファイルを解析中: {api_file_path.name}")
        try:
            api_text = api_file_path.read_text(encoding="utf-8")
            # 各ファイルからグラフデータを抽出
            partial_api_data = _extract_graph_from_specs_with_llm(api_text)

            nodes = partial_api_data.get("nodes", [])
            rels = partial_api_data.get("relationships", [])

            print(f"    -> 抽出結果: ノード={len(nodes)}件, リレーション={len(rels)}件")

            all_nodes.extend(nodes)
            all_relationships.extend(rels)

        except FileNotFoundError:
            print(f"⚠ 警告: {api_file_path} が見つかりませんでした。")
        except Exception as e:
            print(f"⚠ {api_file_path.name} の処理中にエラーが発生しました: {e}")

    # 抽出したデータを統合
    # 重複ノードをIDに基づいてマージする（後勝ち）
    merged_nodes_dict = {}
    for node in all_nodes:
        node_id = node.get("id")
        if node_id:
            if node_id in merged_nodes_dict:
                # 既存のノードプロパティを更新（マージ）
                merged_nodes_dict[node_id].setdefault("properties", {}).update(node.get("properties", {}))
            else:
                merged_nodes_dict[node_id] = node

    merged_nodes = list(merged_nodes_dict.values())

    # 重複リレーション（source, target, typeが同一）を削除
    seen_rels = set()
    merged_relationships = []
    for rel in all_relationships:
        rel_tuple = (rel.get("source"), rel.get("target"), rel.get("type"))
        if rel.get("source") and rel.get("target") and rel.get("type") and rel_tuple not in seen_rels:
            merged_relationships.append(rel)
            seen_rels.add(rel_tuple)

    api_data_from_llm = {
        "nodes": merged_nodes,
        "relationships": merged_relationships
    }

    print(f"✔ 統合後のAPI仕様書データ: ノード={len(merged_nodes)}件, リレーション={len(merged_relationships)}件")

    # データ型の説明テキストを読み込む
    api_arg_text = _read_api_arg_text()
    print("🤖 LLMによるデータ型説明 (api_arg.txt) の抽出を実行中...")
    type_descriptions = _extract_datatype_descriptions_with_llm(api_arg_text)

    # LLMが生成したデータにデータ型の説明を追加
    for node in api_data_from_llm.get("nodes", []):
        if node.get("type") == "DataType" and node.get("properties", {}).get("name") in type_descriptions:
            node["properties"]["description"] = type_descriptions[node["properties"]["name"]]

    # LLMの出力を後続処理用のトリプル形式に変換
    spec_triples, spec_node_props = extract_triples_from_specs(api_data_from_llm, type_descriptions)

    print(f"✔ API仕様書からトリプルを生成: {len(spec_triples)} 件")

    # Neo4jに投入する前のAPI仕様書由来のデータ(トリプルとノードプロパティ)をJSONファイルとして保存
    data_to_save = {
        "relationships": spec_triples,
        "nodes": spec_node_props
    }
    with open("neo4j_data.json", "w", encoding="utf-8") as f:
        json.dump(
            data_to_save,
            f,
            indent=2,
            ensure_ascii=False,
        )
    print("💾 API仕様書解析後のデータ(トリプル/ノード)を 'neo4j_data.json' に保存しました。")

    # --- 2. データの統合とグラフDBへの投入 ---
    print("\n🔗 データを統合してグラフを構築中...")

    # Chroma用にデータをまとめる
    all_triples = spec_triples
    all_node_props = spec_node_props

    # Neo4j用のGraphDocumentを生成
    gdocs = _triples_to_graph_documents(all_triples, all_node_props)

    try:
        node_count, rel_count = _rebuild_graph_in_neo4j(gdocs)
        print(f"✔ グラフデータベースの再構築が完了しました: ノード={node_count}, リレーションシップ={rel_count}")
    except ServiceUnavailable as se:
        print(f"⚠ Neo4j への接続に失敗しました: {se}")
        print("   Neo4jサーバーが起動しているか確認してください。")
        return gdocs, all_triples, all_node_props
    except Exception as e:
        print(f"⚠ グラフデータベースの構築中にエラーが発生しました: {e}")
        return gdocs, all_triples, all_node_props

    # --- 4. Help HTML & BracketType の追加（MERGE、削除なし）---
    print("\n📚 Help HTML / BracketType の統合を開始します...")

    try:
        graph_conn = Neo4jGraph(
            url=NEO4J_URI,
            username=NEO4J_USER,
            password=NEO4J_PASSWORD,
            database=NEO4J_DATABASE,
        )

        # 既存APIノード名を取得（DESCRIBES マッチング用）
        method_results = graph_conn.query("MATCH (m:Method) RETURN m.name AS name")
        existing_methods = [r["name"] for r in method_results if r.get("name")]
        object_results = graph_conn.query("MATCH (o:Object) RETURN o.name AS name")
        existing_objects = [r["name"] for r in object_results if r.get("name")]
        print(f"  既存APIノード: Method={len(existing_methods)}, Object={len(existing_objects)}")

        # Phase 1: Help HTML パース
        print("\n  [Phase 1] Help HTML を解析中...")
        help_pages = _parse_help_directory(HELP_DIR)
        print(f"  ✔ {len(help_pages)} ページを解析しました")

        # Phase 2: BracketType 参照テーブルパース
        print("\n  [Phase 2] ブラケット型番参照テーブルをパース中...")
        bracket_triples, bracket_node_props = _parse_bracket_type_reference(BRACKET_TYPE_REF_PATH)

        # Phase 4: Tier2 LLM バッチ抽出（summary / keywords / DESCRIBES）
        print("\n  [Phase 4] Tier2ページ（about_, sample_）のLLM抽出を実行中...")
        help_pages, llm_rels = _extract_help_summaries_with_llm(
            help_pages, existing_methods, existing_objects
        )
        print(f"  ✔ LLM生成 DESCRIBES リレーション: {len(llm_rels)} 件")

        # Phase 3+5: トリプル生成 → GraphDocument → Neo4j MERGE
        print("\n  [Phase 3+5] トリプル生成 & Neo4j への追加 (MERGE)...")
        help_triples, help_node_props = _help_pages_to_triples(
            help_pages, llm_rels, bracket_node_props, existing_methods, existing_objects
        )

        help_gdocs = _triples_to_graph_documents(help_triples, help_node_props)
        graph_conn.add_graph_documents(help_gdocs)

        res_nodes = graph_conn.query("MATCH (n) RETURN count(n) AS c")
        res_rels = graph_conn.query("MATCH ()-[r]->() RETURN count(r) AS c")
        print(
            f"  ✔ Help/Bracket追加後: "
            f"ノード={res_nodes[0]['c']}, リレーション={res_rels[0]['c']}"
        )

        # all_triples / all_node_props にも Help データを追記（ChromaDB用）
        all_triples = all_triples + help_triples
        all_node_props = {**all_node_props, **help_node_props}

    except ServiceUnavailable as se:
        print(f"  ⚠ Neo4j Help追加に失敗しました（接続エラー）: {se}")
    except Exception as e:
        import traceback
        print(f"  ⚠ Help/Bracket追加中にエラーが発生しました: {e}")
        traceback.print_exc()

    # gdocsだけでなく、生のtriplesとnode_propsも返す
    return gdocs, all_triples, all_node_props

def main() -> None:
    # --- Neo4j構築プロセス ---
    # Neo4jを構築し、その過程で生成された生のtriplesとnode_propsも受け取る
    _, all_triples, all_node_props = _build_and_load_neo4j()

    # --- ChromaDB構築プロセス ---
    # gdocsではなく、生のtriplesとnode_propsを渡してChromaDBを構築する
    _build_and_load_chroma(all_triples, all_node_props)

if __name__ == "__main__":
    main()
