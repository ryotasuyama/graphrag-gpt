from tree_sitter import Language, Parser
import tree_sitter_python as tspython

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
# LLMGraphTransformer をインポート
from langchain_experimental.graph_transformers import LLMGraphTransformer

DATA_DIR = Path("data")
NEO4J_URI = config.NEO4J_URI
NEO4J_USER = config.NEO4J_USER
NEO4J_PASSWORD = config.NEO4J_PASSWORD
NEO4J_DATABASE = getattr(config, "NEO4J_DATABASE", "neo4j")

# (削除) api.txt 関連の定義 (API_TXT_CANDIDATES)
# (削除) api_arg.txt 関連の定義 (API_ARG_TXT_CANDIDATES)

PY_LANGUAGE = Language(tspython.language())
parser = Parser(PY_LANGUAGE)

CHROMA_PERSIST_DIR = DATA_DIR / "chroma_db"
OPENAI_API_KEY = config.OPENAI_API_KEY

llm = ChatOpenAI(
    temperature=0, 
    model_name="gpt-5", 
    openai_api_key=OPENAI_API_KEY,
    # request_timeout=600
) 

# (削除) _read_api_arg_text()

def _read_script_files() -> List[Tuple[str, str]]:
    """data ディレクトリ内の .py ファイルをすべて読み込む"""
    script_files = []
    if not DATA_DIR.exists():
        return []
    
    for p in DATA_DIR.glob("*.py"):
        if p.is_file():
            script_files.append((p.name, p.read_text(encoding="utf-8")))
            
    return script_files

def extract_triples_from_script(
    script_path: str, script_text: str
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    """スクリプト例のテキストから、ノード/リレーションのトリプルを生成する (変更なし)"""
    triples: List[Dict[str, Any]] = []
    node_props: Dict[str, Dict[str, Any]] = {}

    script_node_id = script_path
    node_props[script_node_id] = {
        "type": "ScriptExample",
        "properties": {
            "name": script_path,
            "code": script_text
        }
    }

    all_methods_in_script = set()

    # データフローを追跡するため、スクリプト内で変数がどのメソッド呼び出しから生成されたかを記録する
    # { "変数名": "生成元のMethodCallノードID" }
    variable_to_source_call_id: Dict[str, str] = {}

    method_calls_in_script = _extract_method_calls_from_script(script_text)
    prev_call_node_id = None

    for i, call in enumerate(method_calls_in_script):
        method_name = call["method_name"]
        all_methods_in_script.add(method_name)
        
        call_node_id = f"{script_path}_call_{i}"
        node_props[call_node_id] = {
            "type": "MethodCall",
            "properties": {"code": call["full_text"], "order": i}
        }
        
        # ScriptExampleノードに直接CONTAINSリレーションで関連付ける
        triples.append({
            "source": script_node_id, "source_type": "ScriptExample",
            "label": "CONTAINS", "target": call_node_id, "target_type": "MethodCall"
        })
        
        triples.append({
            "source": call_node_id, "source_type": "MethodCall",
            "label": "CALLS", "target": method_name, "target_type": "Method"
        })

        # --- データフロー解析 ---
        # 1. 現在のメソッド呼び出しの引数を解析する
        arguments_node = call["node"].child_by_field_name("arguments")
        if arguments_node:
            # 引数ノード内のすべての変数名（identifier）を再帰的に探索
            arg_vars = []
            def find_identifiers(n):
                if n.type == 'identifier':
                    arg_vars.append(n.text.decode('utf8'))
                for child in n.children:
                    find_identifiers(child)
            find_identifiers(arguments_node)
            
            # 見つかった変数について、それが以前のメソッド呼び出しの結果であるかチェック
            for var_name in set(arg_vars): # setで重複したリレーションを防止
                if var_name in variable_to_source_call_id:
                    source_call_node_id = variable_to_source_call_id[var_name]
                    # データフローを示す PASSES_RESULT_TO リレーションを追加
                    triples.append({
                        "source": source_call_node_id, "source_type": "MethodCall",
                        "label": "PASSES_RESULT_TO", 
                        "target": call_node_id, "target_type": "MethodCall"
                    })

        # 2. 現在のメソッド呼び出しの結果が変数に代入されているかチェック
        if call["assigned_to"]:
            # 変数名と現在の呼び出しIDをマッピングし、後続の呼び出しで参照できるようにする
            variable_to_source_call_id[call["assigned_to"]] = call_node_id
        # --- データフロー解析ここまで ---

        if prev_call_node_id:
            triples.append({
                "source": prev_call_node_id, "source_type": "MethodCall",
                "label": "NEXT", "target": call_node_id, "target_type": "MethodCall"
            })
        
        prev_call_node_id = call_node_id

    for method_name in all_methods_in_script:
        triples.append({
            "source": script_node_id, "source_type": "ScriptExample",
            "label": "IS_EXAMPLE_OF", "target": method_name, "target_type": "Method"
        })

    return triples, node_props


# (削除) _extract_graph_from_specs_with_llm()

# (削除) _extract_datatype_descriptions_with_llm()

# (削除) extract_triples_from_specs()


def _extract_method_calls_from_script(script_text: str) -> List[Dict[str, Any]]:
    """
    スクリプトテキストを解析し、メソッド呼び出しの詳細情報を抽出する。
    提案1の実装：メソッド呼び出しの結果が代入される変数名も取得する。(変更なし)
    """
    tree = parser.parse(bytes(script_text, "utf8"))
    root_node = tree.root_node
    calls = []
    
    def find_calls(node):
        # メソッド呼び出し (`call`ノード) を探す
        if node.type == 'call':
            function_node = node.child_by_field_name('function')
            # obj.method() の形式 (`attribute`ノード) であることを確認
            if function_node and function_node.type == 'attribute':
                obj_node = function_node.child_by_field_name('object')
                method_node = function_node.child_by_field_name('attribute')
                
                if obj_node and method_node:
                    call_details = {
                        "object_name": obj_node.text.decode('utf8'),
                        "method_name": method_node.text.decode('utf8'),
                        "full_text": node.text.decode('utf8'),
                        "node": node,  # データフロー解析のためにnodeオブジェクト自体を保持
                        "assigned_to": None, # 結果が代入される変数名（デフォルトはNone）
                    }
                    
                    # この呼び出しが代入文の一部かチェック (e.g., var = obj.method())
                    parent = node.parent
                    if parent and parent.type == 'assignment':
                        left_node = parent.child_by_field_name('left')
                        if left_node:
                            call_details["assigned_to"] = left_node.text.decode('utf8')
                            
                    calls.append(call_details)

        # 再帰的に子ノードを探索
        for child in node.children:
            find_calls(child)

    find_calls(root_node)
    return calls


def _triples_to_graph_documents(triples: List[Dict[str, Any]], node_props: Dict[str, Dict[str, Any]]) -> List[GraphDocument]:
    """(変更なし)"""
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
    """(変更なし)"""
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

def _build_and_load_chroma(graph_docs: List[GraphDocument]) -> None:
    """
    グラフドキュメントのノード情報からベクトルを生成し、ChromaDBに保存する (変更なし)
    """
    print("\n🚀 ChromaDBのベクトルデータを生成・保存中...")

    if CHROMA_PERSIST_DIR.exists():
        shutil.rmtree(CHROMA_PERSIST_DIR)
    CHROMA_PERSIST_DIR.mkdir(exist_ok=True)

    docs_for_vectorstore: List[Document] = []
    
    if not graph_docs:
        print("⚠ グラフドキュメントが見つからないため、ChromaDBの構築をスキップします。")
        return

    # gdoc (GraphDocument) のノードをベクトル化の対象にする
    print(f"✔ グラフから {len(graph_docs[0].nodes)} 個のノードをベクトル化の対象とします。")
    for node in graph_docs[0].nodes:
        props = node.properties
        content = ""
        # ノードのタイプに応じて、ベクトル化するテキストの内容を整形
        if node.type == "Method":
            content = f"APIメソッド\nメソッド名: {props.get('name', '')}\n説明: {props.get('description', '')}"
        elif node.type == "ScriptExample":
            content = f"スクリプト例\nファイル名: {props.get('name', '')}\n全文コード:\n```python\n{props.get('code', '')}\n```"
        else:
            # その他のノードタイプはプロパティを平文化
            prop_text = "\n".join([f"- {key}: {value}" for key, value in props.items()])
            content = f"ノードタイプ: {node.type}\nID: {node.id}\nプロパティ:\n{prop_text}"
        
        metadata = {
            "source": "graph_node",
            "node_id": node.id,
            "node_type": node.type,
        }
        docs_for_vectorstore.append(Document(page_content=content.strip(), metadata=metadata))

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

def _merge_graph_documents(list_a: List[GraphDocument], list_b: List[GraphDocument]) -> List[GraphDocument]:
    """
    (追加) 複数のGraphDocumentリストを1つにマージし、ノードの重複を排除する
    """
    all_nodes_map: Dict[str, Node] = {}
    all_rels: List[Relationship] = []

    for gdoc in list_a + list_b:
        for node in gdoc.nodes:
            if node.id not in all_nodes_map:
                all_nodes_map[node.id] = node
            else:
                # 既存ノードのプロパティをマージ/更新
                all_nodes_map[node.id].properties.update(node.properties)
        all_rels.extend(gdoc.relationships)

    # 重複リレーションを削除 (source.id, target.id, typeが同一)
    seen_rels_set = set()
    unique_rels: List[Relationship] = []
    for rel in all_rels:
        # source/targetがNodeオブジェクトであることを確認
        if isinstance(rel.source, Node) and isinstance(rel.target, Node):
            rel_tuple = (rel.source.id, rel.target.id, rel.type)
            if rel_tuple not in seen_rels_set:
                unique_rels.append(rel)
                seen_rels_set.add(rel_tuple)
        
    merged_gdoc = GraphDocument(
        nodes=list(all_nodes_map.values()),
        relationships=unique_rels,
        source=Document(page_content="Combined API Spec and Example graph")
    )
    # Neo4j/Chromaへの投入関数はリストを期待するためリストで返す
    return [merged_gdoc]

def _build_and_load_neo4j() -> List[GraphDocument]:
    """
    (変更) API仕様とスクリプト例を解析し、Neo4jにグラフを構築する。
    API仕様書の解析にLLMGraphTransformer(カスタムプロンプトなし)を使用する。
    """
    # --- 1. API仕様書 (api*.txt) の解析 (LangChain標準トランスフォーマー使用) ---
    print("📄 API仕様書を解析中 (LangChain標準機能)...")

    # 4つのAPI仕様書ファイルを定義
    api_txt_files = [
        DATA_DIR / "api1.txt",
        DATA_DIR / "api2.txt",
        DATA_DIR / "api3.txt",
        DATA_DIR / "api4.txt",
        DATA_DIR / "api5.txt",
    ]
    
    # LLMGraphTransformerの初期化 (カスタムプロンプトなし)
    llm_transformer = LLMGraphTransformer(llm=llm)

    api_documents: List[Document] = []
    for api_file_path in api_txt_files:
        if not api_file_path.exists():
            print(f"⚠ 警告: {api_file_path} が見つかりません。スキップします。")
            continue
        
        print(f"  - ファイルを読み込み中: {api_file_path.name}")
        try:
            api_text = api_file_path.read_text(encoding="utf-8")
            # LangChainのDocumentオブジェクトとして読み込む
            api_documents.append(Document(page_content=api_text, metadata={"source": api_file_path.name}))
        except Exception as e:
            print(f"⚠ {api_file_path.name} の処理中にエラーが発生しました: {e}")

    print("🤖 LangChainのLLMGraphTransformerによるグラフ抽出を実行中... (カスタムプロンプト不使用)")
    if api_documents:
        # transform_documents は Document ごとに GraphDocument を生成するリストを返す
        spec_gdocs = llm_transformer.convert_to_graph_documents(api_documents)
        print(f"✔ API仕様書から {len(spec_gdocs)} 件のGraphDocument(群)を生成しました。")

        # --- ここから追加 ---
        print("💾 抽出したAPI仕様書データをJSONファイルに出力中...")
        spec_triples_to_save = []
        spec_nodes_to_save = {}
        
        # spec_gdocs は GraphDocument のリスト
        for gdoc in spec_gdocs:
            # 1. ノードを処理 (node_props形式に)
            for node in gdoc.nodes:
                if node.id not in spec_nodes_to_save:
                    spec_nodes_to_save[node.id] = {
                        "type": node.type if node.type else "Unknown", # typeがNoneの場合を考慮
                        "properties": node.properties
                    }
                else:
                    # 既存ノードのプロパティをマージ
                    spec_nodes_to_save[node.id].setdefault("properties", {}).update(node.properties)
            
            # 2. リレーションを処理 (triples形式に)
            for rel in gdoc.relationships:
                # Relationshipオブジェクトのsource/targetはNodeオブジェクト
                source_node = rel.source
                target_node = rel.target
                
                # ノードタイプが None の場合、デフォルト値（例: 'Unknown'）を設定
                source_type = source_node.type if source_node.type else "Unknown"
                target_type = target_node.type if target_node.type else "Unknown"

                spec_triples_to_save.append({
                    "source": source_node.id,
                    "source_type": source_type,
                    "label": rel.type,
                    "target": target_node.id,
                    "target_type": target_type,
                })

        # JSONファイルとして保存 (ingest1025.py と同じ形式)
        data_to_save = {
            "relationships": spec_triples_to_save,
            "nodes": spec_nodes_to_save
        }
        # (json はファイル上部で import 済み)
        with open("neo4j_default_data.json", "w", encoding="utf-8") as f:
            json.dump(
                data_to_save,
                f,
                indent=2,
                ensure_ascii=False,
            )
        print("💾 デフォルト抽出後のデータ(トリプル/ノード)を 'neo4j_default_data.json' に保存しました。")
        # --- ここまで追加 ---

    else:
        print("⚠ 解析対象のAPI仕様書ファイルが見つからなかったため、API仕様グラフは空です。")
        spec_gdocs = [] # 空のリスト
    
    # (削除) _read_api_arg_text() の呼び出し
    # (削除) _extract_datatype_descriptions_with_llm() の呼び出し
    # (削除) LLMが生成したデータへの説明追加ロジック
    # (削除) extract_triples_from_specs() の呼び出し
    # (削除) neo4j_data.json への保存

    # --- 2. スクリプト例 (data/*.py) の解析 (変更なし) ---
    print("\n🐍 スクリプト例 (data/*.py) を解析中...")
    script_files = _read_script_files()
    if not script_files:
        print("⚠ data ディレクトリに解析対象の .py ファイルが見つかりませんでした。")
        script_triples, script_node_props = [], {}
    else:
        all_script_triples = []
        all_script_node_props = {}
        for script_path, script_text in script_files:
            print(f"  - ファイルを解析中: {script_path}")
            triples, node_props = extract_triples_from_script(script_path, script_text)
            all_script_triples.extend(triples)
            all_script_node_props.update(node_props)
        script_triples = all_script_triples
        script_node_props = all_script_node_props
        print(f"✔ スクリプト例からトリプルを総計: {len(script_triples)} 件")

    # --- 3. データの統合とグラフDBへの投入 ---
    print("\n🔗 データを統合してグラフを構築中...")
    
    # スクリプト例のトリプルをGraphDocumentに変換
    script_gdocs = _triples_to_graph_documents(script_triples, script_node_props)
    
    # (変更) API仕様書(spec_gdocs)とスクリプト例(script_gdocs)をマージ
    gdocs = _merge_graph_documents(spec_gdocs, script_gdocs)
    
    try:
        node_count, rel_count = _rebuild_graph_in_neo4j(gdocs)
        print(f"✔ グラフデータベースの再構築が完了しました: ノード={node_count}, リレーションシップ={rel_count}")
    except ServiceUnavailable as se:
        print(f"⚠ Neo4j への接続に失敗しました: {se}")
        print("   Neo4jサーバーが起動しているか確認してください。")
    except Exception as e:
        print(f"⚠ グラフデータベースの構築中にエラーが発生しました: {e}")

    return gdocs
def main() -> None:
    """(変更なし)"""
    # --- Neo4j構築プロセス ---
    # Neo4jを構築し、その過程で生成されたグラフドキュメント(gdocs)を受け取る
    gdocs = _build_and_load_neo4j()

    # --- ChromaDB構築プロセス ---
    # 受け取ったgdocsを使ってChromaDBを構築する
    _build_and_load_chroma(gdocs)

if __name__ == "__main__":
    main()