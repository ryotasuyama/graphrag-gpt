import sys, os, textwrap, config
import argparse
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma

# --- 更新箇所: モダンなChain構築用関数のインポート ---
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

# --- 更新箇所: ChatPromptTemplateのインポート ---
from langchain_core.prompts import ChatPromptTemplate

from langchain_neo4j import Neo4jGraph
from langchain_neo4j.chains.graph_qa.cypher import GraphCypherQAChain
from neo4j.exceptions import ClientError, CypherSyntaxError

# ---------- 共通 LLM ----------
llm = ChatOpenAI(
    model="gpt-5", 
    temperature=0,
    openai_api_key=config.OPENAI_API_KEY,
)

# ---------- Vector QA (Modernized) ----------
vectordb = Chroma(
    persist_directory="data/chroma_db",
    embedding_function=OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY),
)

# 1. 回答生成用のプロンプト (ChatPromptTemplate)
# {context} は create_stuff_documents_chain によって自動的に注入されます
vector_qa_system_prompt = (
    "あなたは、CADアプリケーション「EvoShip」に関するエキスパートアシスタントです。"
    "以下の取得されたコンテキストを使用して、質問に答えてください。"
    "答えがわからない場合は、わからないと答えてください。"
    "\n\n"
    "{context}"
)

vector_qa_prompt = ChatPromptTemplate.from_messages([
    ("system", vector_qa_system_prompt),
    ("human", "{input}"),
])

# 2. ドキュメント結合チェーンの作成
question_answer_chain = create_stuff_documents_chain(llm, vector_qa_prompt)

# 3. リトリーバルチェーンの作成 (これが旧 RetrievalQA の代わりとなります)
retriever = vectordb.as_retriever()
vector_qa_chain = create_retrieval_chain(retriever, question_answer_chain)


# ---------- Graph QA (Modernized Prompts) ----------
graph = Neo4jGraph(
    url=config.NEO4J_URI,
    username=config.NEO4J_USER,
    password=config.NEO4J_PASSWORD,
)

# Cypher生成用プロンプト (ChatPromptTemplate化)
# Systemメッセージに役割とスキーマ情報を集約します
CYPHER_GEN_SYSTEM_MSG = """
あなたは、CADアプリケーション「EvoShip」のAPIに関する知識グラフを熟知したエキスパートです。
ユーザーの質問を解釈し、提供されたグラフスキーマ情報に基づいて、その答えを見つけるための最適なCypherクエリを生成するタスクを担います。

## グラフスキーマ情報
以下に、利用可能なノードラベル、プロパティ、およびリレーションシップタイプの情報を示します。クエリは**必ずこのスキーマ情報に厳密に従って**生成してください。
{schema}

## クエリ生成の指示
1.  **思考プロセスに従う:**
    -   **Step 1. 意図の理解:** ユーザーが「何を知りたいのか」を特定します。
    -   **Step 2. キーワード抽出:** 質問から重要なキーワードを抽出します。
    -   **Step 3. スキーマとのマッピング:** キーワードをスキーマ情報と照らし合わせます。
    -   **Step 4. クエリ生成:** `toLower()` と `CONTAINS` を活用して検索します。

2.  **検索戦略のヒント:**
    -   「方法」「やり方」 -> `Method`ノードの `description`
    -   「サンプルコード」 -> `ScriptExample`ノード (`IS_EXAMPLE_OF`リレーション)
    -   概念 -> `Entity` ノード

## 出力要件
-   生成されたCypherクエリのみを**文字列としてそのまま出力してください。**
-   説明、前置き、Markdownコードブロック(` ```cypher `)は含めないでください。
"""

cypher_generation_prompt = ChatPromptTemplate.from_messages([
    ("system", CYPHER_GEN_SYSTEM_MSG),
    ("human", "質問: {question}"),
])

# 回答生成用プロンプト (ChatPromptTemplate化)
QA_SYSTEM_MSG = """
あなたは、CADアプリケーション「EvoShip」に関するエキスパートアシスタントです。
以下の情報を基に、ユーザーの質問に対して自然な日本語で分かりやすく回答してください。

ナレッジグラフから取得した関連情報:
{context}
"""

cypher_qa_prompt = ChatPromptTemplate.from_messages([
    ("system", QA_SYSTEM_MSG),
    ("human", "ユーザーの要求: {question}"),
])

# GraphQAチェーンの構築
graph_qa = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    verbose=True,
    cypher_prompt=cypher_generation_prompt, # ChatPromptTemplateを渡す
    qa_prompt=cypher_qa_prompt,             # ChatPromptTemplateを渡す
    allow_dangerous_requests=True,
    top_k=10000,
)

# ---------- ルート選択と実行 ----------

def execute_graph_qa(question: str, is_retry: bool = False):
    """
    GraphCypherQAChainを実行し、エラーハンドリングとリトライを行う。
    """
    try:
        # GraphCypherQAChainは従来通り "query" を受け付ける場合が多いが、
        # プロンプト内の変数名に合わせて invoke する
        return graph_qa.invoke({"query": question})
    except (ClientError, CypherSyntaxError) as e:
        print(f"\n--- [Error] An error occurred during graph query: {e} ---")
        
        if is_retry:
            print("--- [Error] Retry failed. Raising exception. ---")
            raise e

        print("--- [Info] Attempting to fix the query by regenerating... ---")
        new_question = f"""
        以下のCypherクエリを実行したところ、Neo4jデータベースでエラーが発生しました。
        エラーメッセージを参考に、正しいCypherクエリを再生成してください。

        【エラー内容】
        {e}

        【元の質問】
        {question}
        """
        return execute_graph_qa(new_question, is_retry=True)


def ask(question: str, route: str = "graph") -> str:
    """
    指定されたルート（検索方法）に基づいて質問に回答します。
    """
    route = route.lower()
    final_question = question

    if route == "graph":
        print("--- [Route: graph] Running Graph Search ---")
        result = execute_graph_qa(final_question)
        return result['result']

    elif route == "vector":
        print("--- [Route: vector] Running Vector Search ---")
        # create_retrieval_chain は "input" をキーとして受け取ります
        # 出力は "answer" キーに含まれます ("result" ではありません)
        response = vector_qa_chain.invoke({"input": final_question})
        
        # コンテキストの確認用出力（デバッグ用）
        if 'context' in response:
             print("\n--- Retrieved Context ---")
             for doc in response['context']:
                 print(f"--- Document ---\n{doc.page_content[:200]}...") # 長すぎるので省略表示
             print("-------------------------\n")
             
        return response['answer']

    elif route == "hybrid":
        print("--- [Route: hybrid] Running Hybrid Search (Vector -> Graph) ---")
        
        print("Step 1/3: Retrieving context from vector store using the question...")
        # ハイブリッド検索の前処理として、ベクトル検索だけを手動で行う（ここはChainを使わなくて良い）
        retriever = vectordb.as_retriever()
        docs = retriever.invoke(question) # get_relevant_documents は invoke に統一されました
        
        if docs:
            retrieved_context_str = "\n\n".join([f"--- Document ---\n{doc.page_content}" for doc in docs])
            print("\n--- Retrieved Context for Hybrid Search ---")
            print(retrieved_context_str)
            print("-------------------------------------------\n")
        else:
            print("No relevant context found in vector store.")

        vector_context = "\n\n".join([doc.page_content for doc in docs])
        
        if not vector_context:
            print("Step 2/3: No relevant context found. Using original question for graph search.")
            hybrid_question = final_question
        else:
            print("Step 2/3: Augmenting question with retrieved context.")
            hybrid_question = f"""
以下の【ベクトル検索で得られた関連情報】を最優先の参考情報として活用し、元の質問に答えてください。
この情報は、グラフ検索でどのノードやリレーションシップに着目すべきかの重要なヒントとなります。

## 【ベクトル検索で得られた関連情報】
{vector_context}

【元の質問】
{question}
"""
        print("Step 3/3: Executing graph search with augmented question...")
        result = execute_graph_qa(hybrid_question)
        return result['result']

    else:
        raise ValueError("route は 'vector', 'graph', 'hybrid' のみ指定できます。")

# ---------- CLI 入口 ----------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Ask questions about the EvoShip API.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("question", help="The question to ask in quotes.")
    parser.add_argument("route", nargs='?', default="graph", choices=['vector', 'graph', 'hybrid'], help="The search route.")
    
    args = parser.parse_args()

    try:
        answer = ask(args.question, args.route)
        print("\n--- Generated Answer ---")
        print(answer)

    except ValueError as e:
        print(f"\nエラー: {e}")
    except Exception as e:
        print(f"\n予期せぬエラーが発生しました: {e}")