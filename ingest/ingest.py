from pathlib import Path
import re
import json
from typing import List, Dict, Any, Optional, Tuple
import shutil

import config, logging
from langchain_core.documents import Document
from langchain_neo4j import Neo4jGraph
from neo4j.exceptions import ServiceUnavailable
from langchain_community.graphs.graph_document import GraphDocument, Node, Relationship
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

DATA_DIR = Path("data")
NEO4J_URI = config.NEO4J_URI
NEO4J_USER = config.NEO4J_USER
NEO4J_PASSWORD = config.NEO4J_PASSWORD
NEO4J_DATABASE = getattr(config, "NEO4J_DATABASE", "neo4j")

API_TXT_CANDIDATES = [
    Path("/mnt/data/api.txt"),
    Path("api.txt"),
    DATA_DIR / "api.txt",
]


API_ARG_TXT_CANDIDATES = [
    Path("/mnt/data/api_arg.txt"),
    Path("api_arg.txt"),
    DATA_DIR / "api_arg.txt",
]

CHROMA_PERSIST_DIR = DATA_DIR / "chroma_db"
OPENAI_API_KEY = config.OPENAI_API_KEY


def _read_api_text() -> str:
    """api.txt を候補パスから読み込む"""
    for p in API_TXT_CANDIDATES:
        if p.exists():
            return p.read_text(encoding="utf-8")
    raise FileNotFoundError("api.txt が見つかりませんでした。/mnt/data/api.txt または ./api.txt を用意してください。")

def _read_api_arg_text() -> str:
    """api_arg.txt を候補パスから読み込む"""
    for p in API_ARG_TXT_CANDIDATES:
        if p.exists():
            return p.read_text(encoding="utf-8")
    raise FileNotFoundError("api_arg.txt が見つかりませんでした。")

def _normalize_text(text: str) -> str:
    """
    改行/タブ/空白の揺れを正規化。
    - Windows系改行を \n に
    - 行末の空白除去
    - タブ→半角スペース
    - 連続空白（NBSP, 全角スペース含む）→半角スペース1個
    - BOM除去
    """
    text = text.replace("\ufeff", "")  # BOM
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = "\n".join(line.rstrip() for line in text.split("\n"))
    text = text.replace("\t", " ")
    text = re.sub(r"[ \u00A0\u3000]+", " ", text)
    return text

def _to_object_id_from_header(header: str) -> str:
    """
    '■Partオブジェクトのメソッド' → 'Part'
    末尾の 'オブジェクト' や 'のメソッド' を適宜落として Object 名を抽出
    """
    s = header.strip()
    s = re.sub(r"^■", "", s)
    s = s.replace("のメソッド", "")
    s = s.replace("オブジェクト", "")
    return s.strip()

def _guess_return_type_from_desc(desc: str) -> str:
    """
    返り値説明からおおまかに型を推定。
    ・'ID' / 'Id' / '要素ID' 含む → 'ID'
    ・それ以外は '不明'
    """
    d = desc or ""
    if re.search(r"\bID\b", d, flags=re.IGNORECASE) or ("要素ID" in d):
        return "ID"
    return "不明"

def _parse_api_specs(text: str) -> List[Dict[str, Any]]:
    """
    api.txt から以下の構造の配列を返す:
    [
      {
        "object": "Part",
        "title_jp": "船殻のプレートソリッド要素を作成する",
        "name": "CreatePlate",
        "return_desc": "作成したソリッド要素のID",
        "return_type": "ID",
        "params": [
          {"name": "...", "type": "...", "description": "..."},
          ...
        ],
      },
      ...
    ]
    """
    lines = text.split("\n")
    closing_pat = re.compile(r"\)\s*;?(?:\s*//.*)?$")
    param_pat = re.compile(
        r"^([A-Za-z_][A-Za-z0-9_]*)\s*,?\s*//\s*([^:：]+)\s*[:：]\s*(.*)$"
    )
    method_start_pat = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*\($")
    header_pat = re.compile(r"^■.+のメソッド$")
    title_pat = re.compile(r"^〇(.+)$")
    ret_pat = re.compile(r"^返り値[:：]\s*(.+)$")

    current_object = None
    current_title = None
    current_return_desc = None
    collecting_params = False
    current_entry: Optional[Dict[str, Any]] = None
    entries: List[Dict[str, Any]] = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].strip()
        if header_pat.match(line):
            current_object = _to_object_id_from_header(line)
            current_title = None
            current_return_desc = None
            i += 1
            continue
        m_title = title_pat.match(line)
        if m_title:
            current_title = m_title.group(1).strip()
            i += 1
            if i < n:
                m_ret = ret_pat.match(lines[i].strip())
                if m_ret:
                    current_return_desc = m_ret.group(1).strip()
                    i += 1
            continue
        m_start = method_start_pat.match(line)
        if m_start:
            method_name = m_start.group(1)
            current_entry = {
                "object": current_object or "Object",
                "title_jp": current_title or "",
                "name": method_name,
                "return_desc": current_return_desc or "",
                "return_type": _guess_return_type_from_desc(current_return_desc or ""),
                "params": [],
            }
            collecting_params = True
            i += 1
            continue
        if collecting_params and current_entry is not None:
            pm = param_pat.match(line)
            if pm:
                pname, ptype, pdesc = pm.groups()
                current_entry["params"].append(
                    {"name": pname, "type": ptype.strip(), "description": pdesc.strip()}
                )
                if closing_pat.search(line):
                    entries.append(current_entry)
                    current_entry = None
                    collecting_params = False
                i += 1
                continue
            if closing_pat.search(line):
                idx_close = line.rfind(")")
                before = line[:idx_close]
                token = before.split(",")[-1].strip()
                token = re.sub(r"[;,\s]+$", "", token)
                comment = line.split("//", 1)[1].strip() if "//" in line else ""
                synth = f"{token} // {comment}" if comment else token
                pm2 = param_pat.match(synth)
                if pm2:
                    pname, ptype, pdesc = pm2.groups()
                    current_entry["params"].append(
                        {"name": pname, "type": ptype.strip(), "description": pdesc.strip()}
                    )
                entries.append(current_entry)
                current_entry = None
                collecting_params = False
                i += 1
                continue
            i += 1
            continue
        i += 1
    return entries

def _parse_data_type_descriptions(text: str) -> Dict[str, str]:
    """
    api_arg.txt を解析し、データ型名とその説明の辞書を返す。
    例: {"文字列": "通常の文字列", "浮動小数点": "通常の数値", ...}
    """
    descriptions = {}
    current_type = None
    current_desc_lines = []
    
    normalized_text = _normalize_text(text)
    
    for line in normalized_text.split("\n"):
        line = line.strip()
        if not line:
            continue
            
        if line.startswith("■"):
            if current_type and current_desc_lines:
                descriptions[current_type] = "\n".join(current_desc_lines).strip()
            
            current_type = line.replace("■", "").strip()
            current_desc_lines = []
        elif current_type:
            current_desc_lines.append(line)
            
    if current_type and current_desc_lines:
        descriptions[current_type] = "\n".join(current_desc_lines).strip()
        
    return descriptions



def extract_triples_from_specs(
    api_text: str, type_descriptions: Dict[str, str]
) -> Tuple[List[Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    """
    仕様テキストからノード/リレーションのトリプルを生成する。
    DataTypeノードにはapi_arg.txtから抽出した説明(description)を追加する。
    返却:
      triples: [
        {"source": "...", "source_type": "...", "label": "HAS_PARAMETER", "target": "...", "target_type": "..."},
        ...
      ]
      node_props: {
        "Part": {"type": "Object", "properties": {...}},
        "CreatePlate": {"type": "Method", "properties": {...}},
        "文字列": {"type": "DataType", "properties": {"name": "文字列", "description": "通常の文字列"}},
        ...
      }
    """
    entries = _parse_api_specs(api_text)

    triples: List[Dict[str, Any]] = []
    node_props: Dict[str, Dict[str, Any]] = {}

    def _clean_type_name(type_name: str) -> str:
        """'点(2D)' -> '点', '要素(配列)' -> '要素' のように型名から括弧書きを削除する"""
        return re.sub(r"\s*\(.+\)$", "", type_name).strip()

    def create_data_type_node(raw_type_name: str) -> str:
        """
        DataTypeノードの定義を作成し、クリーンな型名を返す。
        ノードが既に存在する場合は何もしない。
        """
        cleaned_type_name = _clean_type_name(raw_type_name)
        if cleaned_type_name not in node_props:
            properties = {"name": cleaned_type_name}
            description = type_descriptions.get(cleaned_type_name)
            if description:
                properties["description"] = description
            node_props[cleaned_type_name] = {"type": "DataType", "properties": properties}
        return cleaned_type_name

    for e in entries:
        obj_name = e["object"] or "Object"
        method_name = e["name"]
        title_jp = e.get("title_jp", "")
        ret_desc = e.get("return_desc", "")
        ret_type_raw = e.get("return_type", "不明")
        params = e.get("params", [])

        # ノード定義
        node_props.setdefault(obj_name, {"type": "Object", "properties": {"name": obj_name}})
        node_props.setdefault(method_name, {"type": "Method", "properties": {"name": method_name, "description": title_jp}})
        ret_node_id = f"{method_name}_ReturnValue"
        node_props.setdefault(ret_node_id, {"type": "ReturnValue", "properties": {"description": ret_desc}})
        
        # 返り値のDataTypeノードを作成
        cleaned_ret_type = create_data_type_node(ret_type_raw)

        # 関係: Method -> Object
        triples.append({
            "source": method_name, "source_type": "Method",
            "label": "BELONGS_TO", "target": obj_name, "target_type": "Object"
        })

        # 関係: Method -HAS_RETURNS-> ReturnValue
        triples.append({
            "source": method_name, "source_type": "Method",
            "label": "HAS_RETURNS", "target": ret_node_id, "target_type": "ReturnValue"
        })

        # 関係: ReturnValue -HAS_TYPE-> DataType
        triples.append({
            "source": ret_node_id, "source_type": "ReturnValue",
            "label": "HAS_TYPE", "target": cleaned_ret_type, "target_type": "DataType"
        })

        # パラメータ
        for i, p in enumerate(params):
            pname = p.get("name") or "Param"
            ptype_raw = p.get("type") or "型"
            pdesc = p.get("description") or ""

            param_node_id = f"{method_name}_{pname}"

            # パラメータノードを定義
            node_props.setdefault(param_node_id, {
                "type": "Parameter",
                "properties": {
                    "name": pname,
                    "description": pdesc,
                    "order": i
                }
            })
            
            # パラメータのDataTypeノードを作成
            cleaned_ptype = create_data_type_node(ptype_raw)

            # 関係: Method -> Parameter
            triples.append({
                "source": method_name, "source_type": "Method",
                "label": "HAS_PARAMETER", "target": param_node_id, "target_type": "Parameter"
            })
            # 関係: Parameter -> DataType
            triples.append({
                "source": param_node_id, "source_type": "Parameter",
                "label": "HAS_TYPE", "target": cleaned_ptype, "target_type": "DataType"
            })

    return triples, node_props

def _triples_to_graph_documents(triples: List[Dict[str, Any]], node_props: Dict[str, Dict[str, Any]]) -> List[GraphDocument]:
    """
    トリプルとノード属性から GraphDocument 群を作る
    """
    node_map: Dict[str, Node] = {}
    for node_id, meta in node_props.items():
        ntype = meta["type"]
        props = meta.get("properties", {})
        node_map[node_id] = Node(id=node_id, type=ntype, properties=props)

    rels: List[Relationship] = []
    for t in triples:
        src = node_map[t["source"]]
        tgt = node_map[t["target"]]
        rels.append(
            Relationship(
                source=src,
                target=tgt,
                type=t["label"],
                properties={}
            )
        )

    doc = Document(page_content="API Spec graph")
    gdoc = GraphDocument(nodes=list(node_map.values()), relationships=rels, source=doc)
    return [gdoc]


def _rebuild_graph_in_neo4j(graph_docs: List[GraphDocument]) -> Tuple[int, int]:
    """
    Neo4j をリセットしてから GraphDocument を投入する
    """
    graph = Neo4jGraph(
        url=NEO4J_URI,
        username=NEO4J_USER,
        password=NEO4J_PASSWORD,
        database=NEO4J_DATABASE,
    )
    
    delete_query = "MATCH (n) DETACH DELETE n"
    graph.query(delete_query)
    
    print(f"\n🚀 Neo4jにデータを投入中...")
    
    graph.add_graph_documents(graph_docs)
    
    res_nodes = graph.query("MATCH (n) RETURN count(n) AS c")
    res_rels = graph.query("MATCH ()-[r]->() RETURN count(r) AS c")
    return int(res_nodes[0]["c"]), int(res_rels[0]["c"])



def _build_and_load_chroma_from_specs(entries: List[Dict[str, Any]]) -> None:
    """
    仕様エントリからベクトルDB (Chroma) を構築・永続化する
    """
    print("\n🚀 ChromaDBのベクトルデータを生成・保存中...")

    if CHROMA_PERSIST_DIR.exists():
        shutil.rmtree(CHROMA_PERSIST_DIR)
    CHROMA_PERSIST_DIR.mkdir(exist_ok=True)

    docs_for_vectorstore: List[Document] = []
    for entry in entries:
        content_parts = [
            f"オブジェクト: {entry['object']}",
            f"メソッド名: {entry['name']}",
            f"説明: {entry['title_jp']}",
            f"返り値: {entry['return_desc']}",
        ]
        if entry['params']:
            param_texts = [f"- {p['name']} ({p['type']}): {p['description']}" for p in entry['params']]
            content_parts.append("パラメータ:\n" + "\n".join(param_texts))
        
        content = "\n".join(content_parts)

        metadata = {
            "object": entry['object'],
            "method_name": entry['name'],
        }
        
        docs_for_vectorstore.append(Document(page_content=content, metadata=metadata))

    try:
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        vectorstore = Chroma.from_documents(
            documents=docs_for_vectorstore,
            embedding=embeddings,
            persist_directory=str(CHROMA_PERSIST_DIR)
        )
        print(f"✔ Chroma DB created and persisted with {len(docs_for_vectorstore)} documents at: {CHROMA_PERSIST_DIR}")
    except Exception as e:
        print(f"⚠ Chroma DBの作成に失敗しました: {e}")

def _build_and_load_neo4j_from_triples(api_text: str, type_descriptions: Dict[str, str]) -> None:
    triples, node_props = extract_triples_from_specs(api_text, type_descriptions)
    gdocs = _triples_to_graph_documents(triples, node_props)

    try:
        node_count, rel_count = _rebuild_graph_in_neo4j(gdocs)
        print(f"✔ Graph DB rebuilt from triples: nodes={node_count}, relationships={rel_count}")
    except ServiceUnavailable as se:
        print(f"Neo4j 接続に失敗しました: {se}")
    except Exception as e:
        print(f"⚠ 検証クエリに失敗しました: {e}")



def main() -> None:
    # api.txt と api_arg.txt を読み込み、正規化
    api_text = _read_api_text()
    api_text = _normalize_text(api_text)
    
    api_arg_text = _read_api_arg_text()
    
    api_entries = _parse_api_specs(api_text)
    type_descriptions = _parse_data_type_descriptions(api_arg_text)

    _build_and_load_neo4j_from_triples(api_text, type_descriptions)
    _build_and_load_chroma_from_specs(api_entries)

if __name__ == "__main__":
    main()