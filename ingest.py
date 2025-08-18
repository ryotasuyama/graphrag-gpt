from pathlib import Path
import re
import json
from typing import List, Dict, Any, Optional, Tuple

import config
from langchain_core.documents import Document
from langchain_neo4j import Neo4jGraph
from neo4j.exceptions import ServiceUnavailable
from langchain_community.graphs.graph_document import GraphDocument, Node, Relationship

# ------------------------------------------------------------
# 0. 設定
DATA_DIR = Path("data")
NEO4J_URI      = config.NEO4J_URI
NEO4J_USER     = config.NEO4J_USER
NEO4J_PASSWORD = config.NEO4J_PASSWORD
# ------------------------------------------------------------

def _normalize_text(text: str) -> str:
    """全角空白や全角コロン等を半角相当へ寄せ、余分な空白を整理する。"""
    if text is None:
        return ""
    # 全角空白 -> 半角空白
    normalized = text.replace("\u3000", " ")
    # Windows改行等の正規化
    normalized = normalized.replace("\r\n", "\n").replace("\r", "\n")
    # タブ -> スペース
    normalized = normalized.replace("\t", " ")
    # 連続スペースの簡易圧縮（コメント部のアラインは不要なため）
    normalized = re.sub(r"[ \u00A0]+", " ", normalized)
    return normalized


def _parse_api_spec(text: str) -> List[Dict[str, Any]]:
    """api.txt を解析して [ { object, method, description, return, params[] } ] の配列へ。

    想定フォーマット（例）:
      ■Partオブジェクトのメソッド
      〇船殻のプレートソリッド要素を作成する
        返り値:作成したソリッド要素のID
        CreatePlate(
              PlateName,     // 文字列：説明
              ...
              bUpdate ); // bool：説明

    戻り値タイプは明示が無いが、ドメイン的に ID を採用する。
    """
    lines = [ln.strip() for ln in _normalize_text(text).split("\n") if ln.strip()]

    object_name = None
    entries: List[Dict[str, Any]] = []
    method_block: Dict[str, Any] | None = None
    collecting_params = False

    # 正規表現
    obj_pat = re.compile(r"^■\s*([A-Za-z0-9_一-龥ぁ-んァ-ヶー]+)オブジェクトのメソッド")
    method_desc_pat = re.compile(r"^[〇○]\s*(.+)$")
    return_pat = re.compile(r"^返り値\s*[:：]\s*(.+)$")
    method_sig_open_pat = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*\(")
    method_sig_line_pat = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*\(")  # safety duplicate
    param_pat = re.compile(
        r"^([A-Za-z_][A-Za-z0-9_]*)\s*,?\s*//\s*([A-Za-z0-9_一-龥ぁ-んァ-ヶー]+)\s*[:：]\s*(.*)$"
    )
    closing_pat = re.compile(r"\)\s*;?$")

    i = 0
    while i < len(lines):
        line = lines[i]

        # オブジェクト名
        m = obj_pat.match(line)
        if m:
            object_name = m.group(1)
            i += 1
            continue

        # メソッド説明（先頭に 〇）
        m = method_desc_pat.match(line)
        if m:
            # 新しいメソッドブロック開始
            method_block = {
                "object": object_name or "Object",
                "method": None,
                "description": m.group(1).strip(),
                "return": {"description": None, "type": "ID"},
                "params": [],
            }
            # 次行で返り値/シグネチャが続く見込み
            i += 1
            continue

        # 返り値
        if method_block and not collecting_params:
            m = return_pat.match(line)
            if m:
                method_block["return"]["description"] = m.group(1).strip()
                i += 1
                continue

        # メソッドシグネチャ開始（説明行が無くても検出できるようにする）
        if not collecting_params:
            if "(" in line and not line.startswith("//"):
                # 例: CreatePlate(
                name = line.split("(", 1)[0].strip()
                if re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", name):
                    if not method_block:
                        method_block = {
                            "object": object_name or "Object",
                            "method": name,
                            "description": "",
                            "return": {"description": None, "type": "ID"},
                            "params": [],
                        }
                    else:
                        method_block["method"] = name
                    collecting_params = True
                    i += 1
                    continue

        # パラメータ収集
        if method_block and collecting_params:
            # 終端: ')' を含む行で終了処理（末尾コメントの有無を問わない）
            if ")" in line:
                # 末尾にパラメータ＋終端コメント形式が載っている場合もある
                part_before = line.split(")", 1)[0].strip()
                if part_before and "//" in line:
                    # 例: bUpdate ); // bool：説明
                    left = part_before.split(",")[-1].strip()
                    comment = line.split("//", 1)[1].strip()
                    # 擬似的に結合して param_pat を通す
                    synth = f"{left} // {comment}"
                    pm = param_pat.match(synth)
                    if pm:
                        pname, ptype, pdesc = pm.groups()
                        method_block["params"].append(
                            {"name": pname, "type": ptype, "description": pdesc.strip()}
                        )
                # ブロックを確定
                entries.append(method_block)
                method_block = None
                collecting_params = False
                i += 1
                continue

            # 通常の引数行
            pm = param_pat.match(line)
            if pm:
                pname, ptype, pdesc = pm.groups()
                method_block["params"].append(
                    {"name": pname, "type": ptype, "description": pdesc.strip()}
                )
                i += 1
                continue

        i += 1

    return entries


def _read_api_text() -> str:
    """data/api.txt を UTF-8 で読み込む。存在しなければ空文字を返す。"""
    api_path = DATA_DIR / "api.txt"
    if not api_path.exists():
        return ""
    return api_path.read_text(encoding="utf-8")


def extract_triples_from_specs(specs: List[Dict[str, Any]]) -> Tuple[List[Dict[str, str]], Dict[str, Dict[str, Any]]]:
    """specs からトリプル群とノード属性を決定的に抽出する。

    返値:
      - triples: {source, source_type, label, target, target_type} の配列
      - node_props: node_id -> {type: Label, properties: {...}}
    """
    triples: List[Dict[str, str]] = []
    node_props: Dict[str, Dict[str, Any]] = {}

    for s in specs:
        object_name: str = s.get("object") or "Object"
        method_name: str = s.get("method") or "Method"
        method_desc: str = s.get("description") or ""
        ret_desc: str = (s.get("return") or {}).get("description") or ""
        ret_type: str = (s.get("return") or {}).get("type") or "ID"
        params: List[Dict[str, str]] = s.get("params") or []

        return_node_id = f"{method_name}_ReturnValue"

        # ノード属性
        node_props.setdefault(object_name, {"type": "Object", "properties": {"name": object_name}})
        node_props.setdefault(method_name, {"type": "Method", "properties": {"name": method_name, "description": method_desc}})
        node_props.setdefault(return_node_id, {"type": "ReturnValue", "properties": {"description": ret_desc}})
        node_props.setdefault(ret_type, {"type": "DataType", "properties": {"name": ret_type}})

        # リレーション
        triples.append({"source": object_name, "source_type": "Object", "label": "HAS_METHOD", "target": method_name, "target_type": "Method"})
        triples.append({"source": method_name, "source_type": "Method", "label": "RETURNS", "target": return_node_id, "target_type": "ReturnValue"})
        triples.append({"source": return_node_id, "source_type": "ReturnValue", "label": "HAS_TYPE", "target": ret_type, "target_type": "DataType"})

        for p in params:
            pname: str = p.get("name") or "Param"
            ptype: str = p.get("type") or "型"
            pdesc: str = p.get("description") or ""

            node_props.setdefault(pname, {"type": "Parameter", "properties": {"name": pname, "description": pdesc}})
            node_props.setdefault(ptype, {"type": "DataType", "properties": {"name": ptype}})

            triples.append({"source": method_name, "source_type": "Method", "label": "HAS_PARAMETER", "target": pname, "target_type": "Parameter"})
            triples.append({"source": pname, "source_type": "Parameter", "label": "HAS_TYPE", "target": ptype, "target_type": "DataType"})

    return triples, node_props


def build_graph_document_from_triples(
    triples: List[Dict[str, str]],
    node_props: Dict[str, Dict[str, Any]],
) -> GraphDocument:
    """トリプルとノード属性から GraphDocument を構築する。"""
    id_to_node: Dict[str, Node] = {}
    nodes: List[Node] = []
    relationships: List[Relationship] = []

    def ensure_node(node_id: str) -> Node:
        node = id_to_node.get(node_id)
        if node is not None:
            return node
        meta = node_props.get(node_id, {"type": "Unknown", "properties": {"name": node_id}})
        node = Node(id=node_id, type=meta.get("type", "Unknown"), properties=meta.get("properties", {}))
        id_to_node[node_id] = node
        nodes.append(node)
        return node

    for t in triples:
        src_id = t["source"]
        dst_id = t["target"]
        rel_type = t["label"]
        src_node = ensure_node(src_id)
        dst_node = ensure_node(dst_id)
        relationships.append(Relationship(source=src_node, target=dst_node, type=rel_type, properties={}))

    # source にはダミー Document を付与
    src_doc = Document(page_content="", metadata={"source": "api.txt"})
    return GraphDocument(nodes=nodes, relationships=relationships, source=src_doc)


def _json_literal(value: Any) -> str:
    """Cypher にインラインで埋め込むための JSON 文字列を返す。"""
    return json.dumps(value, ensure_ascii=False)


def triples_to_cypher(
    triples: List[Dict[str, str]],
    node_props: Dict[str, Dict[str, Any]],
) -> str:
    """与えられたトリプル群から、同等のグラフを構築する Cypher を生成する。"""
    lines: List[str] = []

    # ノードを MERGE
    for node_id, meta in node_props.items():
        label = meta.get("type", "Unknown")
        props = dict(meta.get("properties", {}))
        # id をプロパティにも格納しておく
        props.setdefault("id", node_id)
        lines.append(f"MERGE (n:{label} {{id: {_json_literal(node_id)}}}) SET n += {_json_literal(props)};")

    # リレーションを MERGE
    for t in triples:
        src = t["source"]
        dst = t["target"]
        rel = t["label"]
        lines.append(
            """
MATCH (a {id: %s})
MATCH (b {id: %s})
MERGE (a)-[:%s]->(b);
""".strip()
            % (_json_literal(src), _json_literal(dst), rel)
        )

    return "\n".join(lines)


def _build_and_load_neo4j_from_triples(api_text: str) -> None:
    """api.txt テキストからトリプル抽出→GraphDocument 構築→Neo4j へ投入。"""
    if not api_text.strip():
        raise RuntimeError("api.txt が見つからないか空です。data ディレクトリを確認してください。")

    specs = _parse_api_spec(api_text)
    print(f"✔ Parsed api.txt specs: entries={len(specs)}")
    if not specs:
        print("⚠ 解析結果が空です。フォーマットをご確認ください。")

    triples, node_props = extract_triples_from_specs(specs)
    print(f"✔ Extracted triples: count={len(triples)}")

    # 参考出力: 生成 Cypher
    cypher = triples_to_cypher(triples, node_props)
    print("\n-- Generated Cypher (deterministic) --\n" + cypher + "\n-- End Cypher --\n")

    # GraphDocument を構築して投入
    graph_doc = build_graph_document_from_triples(triples, node_props)

    graph = Neo4jGraph(url=NEO4J_URI, username=NEO4J_USER, password=NEO4J_PASSWORD)
    try:
        graph.query("MATCH (n) DETACH DELETE n")
        print("💡 Neo4j graph cleared")
    except ServiceUnavailable as e:
        raise RuntimeError("Neo4j に接続できません。起動を確認してください") from e

    graph.add_graph_documents([graph_doc], baseEntityLabel=True, include_source=True)

    # 検証
    try:
        node_count = graph.query("MATCH (n) RETURN count(n) AS c")[0]["c"]
        rel_count = graph.query("MATCH ()-[r]-() RETURN count(r) AS c")[0]["c"]
        print(f"✔ Graph DB rebuilt from triples: nodes={node_count}, relationships={rel_count}")
    except Exception as e:
        print(f"⚠ 検証クエリに失敗しました: {e}")


def main() -> None:
    # api.txt を直接読み込み → そのまま投入
    api_text = _read_api_text()
    # 正規化してから解析
    api_text = _normalize_text(api_text)
    _build_and_load_neo4j_from_triples(api_text)


if __name__ == "__main__":
    main()