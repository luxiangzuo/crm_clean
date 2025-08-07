# 🧠 Joja MedTech - RAG 模块说明

本模块为 Joja 智能销售邮件生成系统提供检索增强能力（RAG），用于根据客户问题自动引用公司知识文档，生成个性化销售邮件。

---

## 📁 文件结构说明

```
rag/
├── documents/              # Joja 产品与政策文档（Markdown格式）
│   ├── products/...
│   ├── pricing/...
│   └── ...
│
├── joja_index/             # FAISS 向量索引目录（build_index.py 生成）
│
├── build_index.py          # ✅ 将 documents 文档向量化并构建索引
├── retrieve_docs.py        # ✅ 根据客户问题检索文档段落
```

---

## 🛠 运行流程

### ✦ 第 1 步：构建知识向量索引（仅需一次）

```bash
python rag/build_index.py
```

- 输入：rag/documents/ 中所有 .md 文件
- 输出：rag/joja_index/ 中的向量数据库

---

### ✦ 第 2 步：从知识库中检索相关段落

```python
from rag.retrieve_docs import retrieve_docs

query = "客户咨询 ECG S3 的 CE 认证与安装方式"
docs = retrieve_docs(query, top_k=3)

print(docs)
```

- 输出：匹配 query 的 3 条文档内容段落，可拼接进 prompt

---

## 💡 使用建议

- 向量库构建一次后即可重复使用
- 文档更新后需重新运行 build_index.py
- retrieve_docs 可用于邮件生成、客服问答、FAQ 展示等多种用途

---

## ✅ 依赖环境

推荐环境：Python 3.10  
依赖库（建议写入 requirements.txt）:

```
openai
langchain
faiss-cpu
tiktoken
python-dotenv
```




---

## ✅ 使用方法：

只需访问一次这个链接：

```
http://localhost:8000/hubspot/refresh_token
```

刷新成功后，你就可以再次访问：

```
http://localhost:8000/hubspot/get_contacts
```

🎉 正常返回联系人列表啦！

cd mailbot_crm
conda activate jcore310
cd crm_clean
uvicorn app:app --reload

http://localhost:8000/docs

python api/test.py

uvicorn api.main:app --reload


✅ 启动方式：
uvicorn hubspot_oauth_server:app --reload
然后在浏览器打开：
http://localhost:8000/hubspot/get_contacts




curl -X POST http://localhost:8000/upload-notes-by-email ^
  -H "Content-Type: application/json" ^
  -d @"C:\Users\xiao\crm_clean\data\test_notes.json"


python -m ai.generate_sales_reply

python -m rag.build_index


git add .
git commit -m " 配好 Render 前的上传 GitHub"
git push -u origin main