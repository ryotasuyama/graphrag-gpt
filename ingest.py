
from pathlib import Path
import re
import json
import argparse
from typing import List, Dict, Any, Optional

import config
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_neo4j import Neo4jGraph
from neo4j.exceptions import ServiceUnavailable
from langchain_community.graphs.graph_document import GraphDocument, Node, Relationship

# ------------------------------------------------------------
# 0. 設定
DATA_DIR = Path("data")  # フォルダを指定
CHROMA_DIR        = ".chroma"                      # ベクトル DB 保存先
OPENAI_API_KEY    = config.OPENAI_API_KEY
NEO4J_URI         = config.NEO4J_URI
NEO4J_USER        = config.NEO4J_USER
NEO4J_PASSWORD    = config.NEO4J_PASSWORD
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


def _spec_to_graphish_text(specs: List[Dict[str, Any]]) -> str:
    """抽出仕様の可読化（現状未使用だが将来のデバッグ用に残す）。"""
    out_lines: List[str] = []
    for s in specs:
        object_name: str = s.get("object") or "Object"
        method_name: str = s.get("method") or "Method"
        method_desc: str = s.get("description") or ""
        ret_desc: str = (s.get("return") or {}).get("description") or ""
        ret_type: str = (s.get("return") or {}).get("type") or "ID"
        params: List[Dict[str, str]] = s.get("params") or []

        return_node = f"{method_name}_ReturnValue"

        out_lines.append(f"Object: {object_name}")
        out_lines.append(f"Method: {method_name}")
        if method_desc:
            out_lines.append(f"Method.Description: {method_desc}")
        out_lines.append(f"ReturnValue: {return_node}")
        if ret_desc:
            out_lines.append(f"ReturnValue.Description: {ret_desc}")
        out_lines.append(f"ReturnValue.Type: {ret_type}")

        for p in params:
            pname = p.get("name") or "Param"
            ptype = p.get("type") or "型"
            pdesc = p.get("description") or ""
            out_lines.append(f"Parameter: {pname}")
            out_lines.append(f"Parameter.{pname}.Type: {ptype}")
            if pdesc:
                out_lines.append(f"Parameter.{pname}.Description: {pdesc}")

        out_lines.append("")

    return "\n".join(out_lines).strip()


def preprocess_documents(docs: List[Document]) -> List[Document]:
    """決定的な正規化のみを行い、ドキュメント本文を整える。"""
    processed: List[Document] = []
    for d in docs:
        content = d.page_content or ""
        d.page_content = _normalize_text(content)
        meta = dict(d.metadata or {})
        meta["preprocessed"] = True
        d.metadata = meta
        processed.append(d)
    return processed


def load_text_documents(data_dir: Path) -> List[Document]:
    """dataディレクトリ配下の*.txtをLangChain Documentsとして読み込む。"""
    documents: List[Document] = []
    for file_path in data_dir.glob("*.txt"):
        if file_path.is_file():
            documents.extend(TextLoader(str(file_path)).load())
    return documents


def save_preprocessed_documents(docs: List[Document], out_dir: Path) -> List[Path]:
    """前処理済みドキュメントをファイルとして保存する。

    各`Document.metadata['source']`のベース名を用いて、`out_dir`直下に書き出す。
    既存ファイルは上書きする。
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    written_paths: List[Path] = []
    for d in docs:
        src = str(d.metadata.get("source") or "")
        name = Path(src).name or "document.txt"
        target = out_dir / name
        with target.open("w", encoding="utf-8") as f:
            f.write(d.page_content or "")
        written_paths.append(target)
    return written_paths


def build_graph_json_from_specs(specs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """_parse_api_spec の出力から sample.json と同一構造の JSON を決定的に構築する。"""
    nodes: List[Dict[str, Any]] = []
    relationships: List[Dict[str, str]] = []

    if not specs:
        return {"nodes": nodes, "relationships": relationships}

    # 現状 api.txt は単一オブジェクト・単一メソッド想定
    s = specs[0]
    object_name: str = s.get("object") or "Object"
    method_name: str = s.get("method") or "Method"
    method_desc: str = s.get("description") or ""
    ret_desc: str = (s.get("return") or {}).get("description") or ""
    ret_type: str = (s.get("return") or {}).get("type") or "ID"
    params: List[Dict[str, str]] = s.get("params") or []

    created_node_ids: set[str] = set()

    def add_node(node_id: str, labels: List[str], properties: Dict[str, Any]) -> None:
        if node_id in created_node_ids:
            return
        nodes.append({"id": node_id, "labels": labels, "properties": properties})
        created_node_ids.add(node_id)

    def add_rel(src: str, dst: str, label: str) -> None:
        relationships.append({"source": src, "target": dst, "label": label})

    # ノード: オブジェクト, メソッド, 返り値, 返り値型(ID)
    add_node(object_name, ["Object"], {"name": object_name})
    add_node(method_name, ["Method"], {"name": method_name, "description": method_desc})
    return_node_id = f"{method_name}_ReturnValue"
    add_node(return_node_id, ["ReturnValue"], {"description": ret_desc})
    add_node(ret_type, ["DataType"], {"name": ret_type})

    # リレーション（先頭3件）
    add_rel(object_name, method_name, "HAS_METHOD")
    add_rel(method_name, return_node_id, "RETURNS")
    add_rel(return_node_id, ret_type, "HAS_TYPE")

    # パラメータとデータ型
    for p in params:
        pname: str = p.get("name") or "Param"
        ptype: str = p.get("type") or "型"
        pdesc: str = p.get("description") or ""

        add_node(pname, ["Parameter"], {"name": pname, "description": pdesc})
        # データ型ノードは初出時のみ追加
        add_node(ptype, ["DataType"], {"name": ptype})

        # リレーション（パラメータ関連を順に2本）
        add_rel(method_name, pname, "HAS_PARAMETER")
        add_rel(pname, ptype, "HAS_TYPE")

    return {"nodes": nodes, "relationships": relationships}


def build_graph_document_from_specs(
    specs: List[Dict[str, Any]],
    source: Optional[Document | Dict[str, Any]] = None,
) -> GraphDocument:
    """_parse_api_spec の出力から GraphDocument を決定的に構築する。"""
    if not specs:
        # source は None を許容しないため空の Document を渡す
        src = source if source is not None else Document(page_content="", metadata={"source": "deterministic"})
        return GraphDocument(nodes=[], relationships=[], source=src)

    s = specs[0]
    object_name: str = s.get("object") or "Object"
    method_name: str = s.get("method") or "Method"
    method_desc: str = s.get("description") or ""
    ret_desc: str = (s.get("return") or {}).get("description") or ""
    ret_type: str = (s.get("return") or {}).get("type") or "ID"
    params: List[Dict[str, str]] = s.get("params") or []

    created_node_ids: set[str] = set()
    id_to_node: dict[str, Node] = {}
    nodes: List[Node] = []
    relationships: List[Relationship] = []

    def add_node(node_id: str, node_type: str, properties: Optional[Dict[str, Any]] = None) -> None:
        if node_id in created_node_ids:
            return
        node_obj = Node(id=node_id, type=node_type, properties=properties or {})
        nodes.append(node_obj)
        id_to_node[node_id] = node_obj
        created_node_ids.add(node_id)

    def add_rel(src: str, dst: str, rel_type: str, properties: Optional[Dict[str, Any]] = None) -> None:
        src_node = id_to_node.get(src)
        dst_node = id_to_node.get(dst)
        if src_node is None or dst_node is None:
            # 安全のため存在しなければダミー作成（型は Unknown）
            if src_node is None:
                add_node(src, "Unknown", {"name": src})
                src_node = id_to_node[src]
            if dst_node is None:
                add_node(dst, "Unknown", {"name": dst})
                dst_node = id_to_node[dst]
        relationships.append(
            Relationship(source=src_node, target=dst_node, type=rel_type, properties=properties or {})
        )

    # ノード
    add_node(object_name, "Object", {"name": object_name})
    add_node(method_name, "Method", {"name": method_name, "description": method_desc})
    return_node_id = f"{method_name}_ReturnValue"
    add_node(return_node_id, "ReturnValue", {"description": ret_desc})
    add_node(ret_type, "DataType", {"name": ret_type})

    # リレーション
    add_rel(object_name, method_name, "HAS_METHOD")
    add_rel(method_name, return_node_id, "RETURNS")
    add_rel(return_node_id, ret_type, "HAS_TYPE")

    # パラメータ
    for p in params:
        pname: str = p.get("name") or "Param"
        ptype: str = p.get("type") or "型"
        pdesc: str = p.get("description") or ""

        add_node(pname, "Parameter", {"name": pname, "description": pdesc})
        add_node(ptype, "DataType", {"name": ptype})
        add_rel(method_name, pname, "HAS_PARAMETER")
        add_rel(pname, ptype, "HAS_TYPE")

    src = source if source is not None else Document(page_content="", metadata={"source": "deterministic"})
    return GraphDocument(nodes=nodes, relationships=relationships, source=src)


def export_graph_json_from_api_doc(docs: List[Document], out_path: Path) -> Optional[Path]:
    """ドキュメント群から api.txt を探し、JSON を決定的生成して out_path に保存。"""
    api_doc: Optional[Document] = None
    for d in docs:
        src = str(d.metadata.get("source") or "")
        if src.endswith("api.txt") or src.split("/")[-1] == "api.txt":
            api_doc = d
            break

    if api_doc is None:
        return None

    specs = _parse_api_spec(api_doc.page_content or "")
    data = build_graph_json_from_specs(specs)
    # 既存 sample.json に合わせてインデント/キー順は標準のまま
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return out_path


def index_documents_in_chroma(docs: List[Document]) -> None:
    """前処理済みドキュメントをChromaに登録（OpenAI Embeddings使用）。"""
    from langchain_openai import OpenAIEmbeddings
    from langchain_chroma import Chroma

    Chroma.from_documents(
        docs,
        embedding=OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY),
        persist_directory=CHROMA_DIR,
    )


def rebuild_neo4j_graph_deterministic(docs: List[Document]) -> None:
    """決定的ロジックで GraphDocument を構築し、Neo4j を再構築する。"""
    # api.txt を特定
    api_doc: Optional[Document] = None
    for d in docs:
        src = str(d.metadata.get("source") or "")
        if src.endswith("api.txt") or src.split("/")[-1] == "api.txt":
            api_doc = d
            break

    if api_doc is None:
        raise RuntimeError("api.txt が見つかりませんでした。data ディレクトリを確認してください。")

    specs = _parse_api_spec(api_doc.page_content or "")
    print(f"✔ Parsed specs from api.txt: {len(specs)} entries")
    if specs:
        first = specs[0]
        print(f"  object={first.get('object')} method={first.get('method')} params={len(first.get('params') or [])}")
    doc: GraphDocument = build_graph_document_from_specs(specs, source=api_doc)
    print(f"✔ Deterministic GraphDocument built: nodes={len(doc.nodes)}, relationships={len(doc.relationships)}")
    if len(doc.nodes) == 0:
        print("⚠ 生成された GraphDocument にノードがありません。api.txt のフォーマットをご確認ください。")

    # Neo4j 接続
    graph = Neo4jGraph(
        url=NEO4J_URI,
        username=NEO4J_USER,
        password=NEO4J_PASSWORD,
    )

    # 既存グラフをクリア
    try:
        graph.query("MATCH (n) DETACH DELETE n")
        print("💡 Neo4j graph cleared")
    except ServiceUnavailable as e:
        raise RuntimeError("Neo4j に接続できません。起動を確認してください") from e

    # 追加
    graph.add_graph_documents([doc], baseEntityLabel=True, include_source=True)
    # 検証用にノード/リレーション数を確認
    try:
        node_count = graph.query("MATCH (n) RETURN count(n) AS c")[0]["c"]
        rel_count = graph.query("MATCH ()-[r]-() RETURN count(r) AS c")[0]["c"]
        print(f"✔ Graph DB rebuilt from deterministic spec (api.txt): nodes={node_count}, relationships={rel_count}")
    except Exception as e:
        print(f"⚠ 検証クエリに失敗しました: {e}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest pipeline with optional deterministic JSON export (no LLM)")
    parser.add_argument("--export-json", dest="export_json", type=str, default=None,
                        help="LLM を使わずに api.txt から決定的 JSON を生成して保存する出力先パス")
    # 旧 --no-llm オプションは廃止（常に決定的ロジックを使用）
    parser.add_argument("--preprocess-only", dest="preprocess_only", action="store_true",
                        help="前処理のみ実行。Chroma/LLM/Neo4j 処理を全てスキップする")
    parser.add_argument("--preprocess-out", dest="preprocess_out", type=str, default=None,
                        help="前処理済みテキストを書き出すディレクトリ（指定時はファイル保存する）")
    parser.add_argument("--skip-embeddings", dest="skip_embeddings", action="store_true",
                        help="前処理後のベクトルDB登録（OpenAI Embeddings）をスキップする")
    args = parser.parse_args()
    # 1. ドキュメント読み込み（dataフォルダ内の全ファイル）
    docs = load_text_documents(DATA_DIR)

    # 1-B. 前処理
    docs = preprocess_documents(docs)
    print("✔ Preprocessed text for graph extraction")
    # 1-C. 前処理結果の保存（任意）
    if args.preprocess_out:
        out_dir = Path(args.preprocess_out)
        written = save_preprocessed_documents(docs, out_dir)
        print(f"✔ Wrote {len(written)} preprocessed files -> {out_dir}")

    # 2. ベクトル DB へ登録（Chroma は 0.4+ で自動永続化）
    # 前処理のみ/スキップ指定でない場合のみ実行
    if not args.preprocess_only and not args.skip_embeddings:
        index_documents_in_chroma(docs)
        print("✔ Vector DB updated (.chroma)")

    # 2-B. LLM を使わない決定的 JSON エクスポート
    if args.export_json:
        out_path = export_graph_json_from_api_doc(docs, Path(args.export_json))
        if out_path is None:
            print("⚠ api.txt が見つからないため JSON を出力できませんでした")
        else:
            print(f"✔ Exported deterministic graph JSON -> {out_path}")

    # 前処理のみモードならここで終了
    if args.preprocess_only:
        return

    # 3-5. 決定的ロジックにより Neo4j を再構築
    rebuild_neo4j_graph_deterministic(docs)

if __name__ == "__main__":
    main()
