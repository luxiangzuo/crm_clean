from dotenv import load_dotenv
load_dotenv()
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain_community.vectorstores import FAISS
from utils.embedding_loader import load_embedding_model
from langchain.docstore.document import Document
from langchain.text_splitter import MarkdownHeaderTextSplitter  # 用这个！
# from langchain.text_splitter import CharacterTextSplitter   # 不再使用

def load_markdown_files(root_dir):
    all_chunks = []
    
    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "Section"),
            ("##", "Subsection"),
            ("###", "QA")  # QA级别的问题结构
        ]
    )

    for foldername, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".md"):
                filepath = os.path.join(foldername, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    text = f.read()

                metadata = {
                    "source": os.path.relpath(filepath, root_dir)
                }

                docs = splitter.split_text(text)
                print(f"📄 文档: {metadata['source']} ➤ 切分成 {len(docs)} 段")

                # 添加源文件路径到每段的 metadata
                for doc in docs:
                    doc.metadata["source"] = metadata["source"]
                    all_chunks.append(doc)

    print(f"\n📊 所有文档共切分出 {len(all_chunks)} 个段落。\n")
    return all_chunks

def build_index(doc_dir="documents", index_dir="rag/joja_index"):
    print("🔍 正在加载并切分 Markdown 文档...")
    docs = load_markdown_files(doc_dir)

    if not docs:
        raise ValueError(f"❌ 未找到有效文档，请检查路径是否正确: {doc_dir}")

    print(f"📚 共切分出 {len(docs)} 个段落，开始生成向量...")
    embeddings = load_embedding_model("openai")  # 或 "gemini"
    vectordb = FAISS.from_documents(docs, embeddings)

    vectordb.save_local(index_dir)
    print(f"✅ 向量索引构建完成，保存在 {index_dir}")

if __name__ == "__main__":
    build_index()
