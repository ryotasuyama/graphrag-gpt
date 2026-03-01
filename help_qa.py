"""
EvoShip ヘルプ QA スクリプト

使い方:
  # 単一質問モード
  python help_qa.py "ロフトフィーチャーとはなんですか？"

  # REPL モード（対話的）
  python help_qa.py
  # → "exit" または Ctrl+C で終了
"""

import sys
import re
import config
from typing import List, Optional

from langchain_openai import ChatOpenAI
from langchain_neo4j import Neo4jGraph

# ========== 定数 ==========

SYSTEM_PROMPT = """あなたは CAD アプリケーション「EvoShip」の専門家アシスタントです。
以下のヘルプドキュメント・API 仕様のコンテキストを参照して、ユーザーの質問に日本語で正確・簡潔に回答してください。

コンテキストに答えが見つからない場合は「ヘルプドキュメントには該当情報が見つかりませんでした」と正直に伝えてください。
コード生成は行わず、ヘルプ内容・API 仕様の説明・解釈に専念してください。

"""

_STOP_WORDS_EN = {
    "the", "and", "for", "with", "this", "that", "from", "are", "has",
    "will", "can", "please", "use", "add", "get", "set", "new",
}

# ========== 遅延初期化 ==========

_graph: Optional[Neo4jGraph] = None
_llm: Optional[ChatOpenAI] = None


def _get_graph() -> Neo4jGraph:
    global _graph
    if _graph is None:
        _graph = Neo4jGraph(
            url=config.NEO4J_URI,
            username=config.NEO4J_USER,
            password=config.NEO4J_PASSWORD,
        )
    return _graph


def _get_llm() -> ChatOpenAI:
    global _llm
    if _llm is None:
        _llm = ChatOpenAI(
            model="gpt-5.2",
            temperature=0,
            openai_api_key=config.OPENAI_API_KEY,
        )
    return _llm


# ========== キーワード抽出 ==========

def _extract_search_terms(text: str) -> List[str]:
    """質問テキストから検索用キーワードを抽出する（LLM不使用）"""
    terms: List[str] = []

    # 英語単語（3文字以上）
    for w in re.findall(r"[a-zA-Z]{3,}", text):
        if w.lower() not in _STOP_WORDS_EN:
            terms.append(w)

    # カタカナ語（2文字以上）
    terms.extend(re.findall(r"[\u30a0-\u30ff]{2,}", text))

    # 漢字・ひらがな混じりの語（2文字以上）
    for w in re.findall(r"[\u4e00-\u9fff][\u3040-\u9fff\u4e00-\u9fff]*", text):
        if len(w) >= 2:
            terms.append(w)

    # 重複除去・順序保持
    seen: set = set()
    result: List[str] = []
    for t in terms:
        if t not in seen:
            seen.add(t)
            result.append(t)
    return result[:5]


# ========== CamelCase 抽出 ==========

def _extract_camelcase_terms(text: str) -> List[str]:
    """テキストから CamelCase 語（メソッド名の典型形式）を抽出する"""
    return list(dict.fromkeys(re.findall(r'[A-Z][a-z]+(?:[A-Z][a-z*]+)+', text)))


# ========== ヘルプページ検索 ==========

def search_help_pages(question: str) -> list:
    """
    2段階検索で HelpPage ノードを取得する。

    主検索: keywords / title CONTAINS → 各キーワード最大5件、id重複排除、合計10件まで
    フォールバック: 主検索ゼロ件時のみ raw_text CONTAINS
    """
    graph = _get_graph()
    terms = _extract_search_terms(question)

    seen_ids: set = set()
    pages: list = []

    # 主検索
    for term in terms:
        rows = graph.query(
            "MATCH (h:HelpPage) "
            "WHERE any(kw IN h.keywords WHERE toLower(kw) CONTAINS toLower($term)) "
            "   OR toLower(h.title) CONTAINS toLower($term) "
            "RETURN h.id AS id, h.title AS title, h.summary AS summary, "
            "       h.raw_text AS raw_text, h.page_type AS page_type "
            "LIMIT 5",
            {"term": term},
        )
        for row in rows:
            rid = row.get("id")
            if rid and rid not in seen_ids and len(pages) < 10:
                seen_ids.add(rid)
                pages.append(row)

    # フォールバック（主検索ゼロ件時のみ）
    if not pages:
        for term in terms:
            rows = graph.query(
                "MATCH (h:HelpPage) "
                "WHERE toLower(h.raw_text) CONTAINS toLower($term) "
                "RETURN h.id AS id, h.title AS title, h.summary AS summary, "
                "       h.raw_text AS raw_text, h.page_type AS page_type "
                "LIMIT 5",
                {"term": term},
            )
            for row in rows:
                rid = row.get("id")
                if rid and rid not in seen_ids and len(pages) < 10:
                    seen_ids.add(rid)
                    pages.append(row)
            if pages:
                break

    return pages


# ========== API メソッド検索 ==========

def search_api_methods(question: str) -> list:
    """
    CamelCase 語 + 英語キーワードで Method ノードを検索し、
    パラメータ・戻り値情報を付加して返す。合計 5 メソッドまで。
    """
    graph = _get_graph()

    # 検索語: CamelCase 語を優先し、次に英語キーワード
    camel_terms = _extract_camelcase_terms(question)
    en_terms = [t for t in _extract_search_terms(question) if re.match(r'^[a-zA-Z]', t)]
    search_terms = list(dict.fromkeys(camel_terms + en_terms))

    seen_names: set = set()
    methods: list = []

    for term in search_terms:
        if len(methods) >= 5:
            break
        rows = graph.query(
            "MATCH (m:Method) "
            "WHERE toLower(m.name) CONTAINS toLower($term) "
            "OPTIONAL MATCH (m)-[:BELONGS_TO]->(obj:Object) "
            "OPTIONAL MATCH (m)-[:HAS_RETURNS]->(rv:ReturnValue)-[:HAS_TYPE]->(rt:DataType) "
            "RETURN m.name AS name, m.description AS desc, "
            "       obj.name AS obj_name, "
            "       rv.description AS rv_desc, rt.name AS rv_type "
            "LIMIT 5",
            {"term": term},
        )
        for row in rows:
            name = row.get("name")
            if name and name not in seen_names and len(methods) < 5:
                seen_names.add(name)
                # パラメータを別クエリで取得
                param_rows = graph.query(
                    "MATCH (m:Method {name: $method_name})-[:HAS_PARAMETER]->(p:Parameter) "
                    "OPTIONAL MATCH (p)-[:HAS_TYPE]->(pt:DataType) "
                    "RETURN p.name AS param_name, p.description AS param_desc, "
                    "       p.order AS param_order, pt.name AS param_type "
                    "ORDER BY p.order",
                    {"method_name": name},
                )
                methods.append({**row, "params": param_rows})

    return methods


# ========== コンテキスト整形 ==========

def _build_api_context(methods_data: list) -> str:
    """API メソッド検索結果をプロンプト用テキストに整形する"""
    parts = ["## API 仕様コンテキスト"]
    for m in methods_data:
        name = m.get("name") or "(名称不明)"
        obj_name = m.get("obj_name") or ""
        desc = m.get("desc") or ""
        rv_desc = m.get("rv_desc") or ""
        rv_type = m.get("rv_type") or ""
        params = m.get("params") or []

        header = f"### [API] {name}"
        if obj_name:
            header += f"（オブジェクト: {obj_name}）"
        section = header
        if desc:
            section += f"\n説明: {desc}"

        if params:
            section += "\n引数:"
            for p in params:
                order = p.get("param_order")
                pname = p.get("param_name") or "?"
                ptype = p.get("param_type") or ""
                pdesc = p.get("param_desc") or ""
                prefix = f"  {order}." if order is not None else "  -"
                type_str = f"（{ptype}）" if ptype else ""
                desc_str = f": {pdesc}" if pdesc else ""
                section += f"\n{prefix} {pname}{type_str}{desc_str}"
        else:
            section += "\n引数: なし"

        if rv_desc or rv_type:
            rv_type_str = f"（{rv_type}）" if rv_type else ""
            rv_desc_str = f" - {rv_desc}" if rv_desc else ""
            section += f"\n戻り値: {rv_type_str}{rv_desc_str}"
        else:
            section += "\n戻り値: なし"

        parts.append(section)
    return "\n\n".join(parts)


def _build_context(pages: list) -> str:
    """検索結果ページをプロンプト用テキストに整形する"""
    if not pages:
        return "（関連するヘルプページが見つかりませんでした）"

    parts = []
    for i, page in enumerate(pages, 1):
        title = page.get("title") or "(タイトルなし)"
        summary = page.get("summary") or ""
        raw_text = page.get("raw_text") or ""

        # raw_text は最大 800 文字にトリミング
        if len(raw_text) > 800:
            raw_text = raw_text[:800] + "..."

        section = f"### [{i}] {title}"
        if summary:
            section += f"\n概要: {summary}"
        if raw_text:
            section += f"\n本文抜粋:\n{raw_text}"
        parts.append(section)

    return "\n\n".join(parts)


# ========== メイン QA 関数 ==========

def answer_question(question: str) -> str:
    """
    Neo4j の HelpPage を検索し、LLM で回答を生成して返す。
    エラー時は日本語エラー文字列を返す（例外を外に出さない）。
    """
    try:
        pages = search_help_pages(question)
        methods = search_api_methods(question)
    except Exception as e:
        return f"[エラー] Neo4j への接続またはクエリ実行に失敗しました: {e}"

    print(f"--- [{len(pages)}件のヘルプページ、{len(methods)}件のAPIメソッドを参照] ---")

    context_parts = []
    if methods:
        context_parts.append(_build_api_context(methods))
    if pages:
        context_parts.append("## ヘルプドキュメント コンテキスト\n\n" + _build_context(pages))

    context = "\n\n".join(context_parts) if context_parts else "（関連情報が見つかりませんでした）"

    prompt = (
        SYSTEM_PROMPT
        + context
        + "\n\n## 質問\n\n"
        + question
    )

    try:
        llm = _get_llm()
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"[エラー] LLM の呼び出しに失敗しました: {e}"


# ========== CLI エントリポイント ==========

def main() -> None:
    if len(sys.argv) > 1:
        # 単一質問モード
        question = " ".join(sys.argv[1:])
        print(answer_question(question))
    else:
        # REPL モード
        print("EvoShip ヘルプ QA モード（'exit' または Ctrl+C で終了）")
        while True:
            try:
                question = input("\n質問: ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\n終了します。")
                break
            if not question:
                continue
            if question.lower() == "exit":
                print("終了します。")
                break
            print()
            print(answer_question(question))


if __name__ == "__main__":
    main()
