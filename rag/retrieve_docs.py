# rag/retrieve_docs.py
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
def load_vectorstore(index_path="rag/joja_index"):
    embeddings = OpenAIEmbeddings()
    return FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)

def retrieve_docs(query, top_k=5, score_threshold=2.2, debug=True, fallback_text=None):
    db = load_vectorstore()
    results_with_score = db.similarity_search_with_score(query, k=top_k)

    filtered = []
    for i, (doc, score) in enumerate(results_with_score):
        if score <= score_threshold:
            filtered.append(doc)
        else:
            if debug:
                print(f"❌ 丢弃低相关段落（score={score:.4f}）: {doc.page_content[:50]}...")

    if not filtered:
        print("⚠️ RAG 没有召回任何文档！模型即将自由发挥！🚨")
        if fallback_text:
            print("🚨 使用 fallback 内容替代文档片段。")
            return fallback_text

    if debug:
        print(f"\n✅ 最终保留段落数：{len(filtered)}")
        print("\n📚 最终召回段落内容如下：")
        for i, doc in enumerate(filtered):
            print(f"\n[段落 {i+1}] 来自 {doc.metadata.get('source', '')}")
            print(doc.page_content)
            print("---")

    return "\n\n".join([f"[{i+1}] {doc.page_content}" for i, doc in enumerate(filtered)])
