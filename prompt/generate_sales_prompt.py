# generate_sales_prompt.py

import json
from rag.retrieve_docs import retrieve_docs


def build_prompt(customer_info, email_summary, style="professional", max_docs=3, debug=False):
    """
    构造用于销售邮件生成的 prompt。
    - customer_info: 客户信息 dict
    - email_summary: 客户意图/上封邮件摘要 dict
    - style: 语气控制（professional / friendly / concise）
    - max_docs: RAG 检索的文档数量
    """
    query = f"{email_summary.get('主题', '')}\n\n{email_summary.get('正文', '')}"

    

    fallback = (
    "* No relevant product or pricing documents were found.\n"
    "Please inform the customer that our sales representative will assist with accurate details shortly."
        )

    rag_context = retrieve_docs(query, top_k=max_docs, debug=debug, fallback_text=fallback)


    prompt = f"""
You are a sales representative at Joja MedTech Inc. Your task is to write a professional follow-up email in response to the customer's message. The customer has raised several specific questions, and you should address each of them clearly and thoroughly.

--- Customer Info ---
{json.dumps(customer_info, indent=2, ensure_ascii=False)}

--- Customer Email Subject ---
{email_summary.get("主题", "N/A")}

--- Customer Email Body ---
{email_summary.get("正文", "N/A")}

--- Internal Knowledge Base Snippets ---
{rag_context}

--- Instructions ---
1. Carefully read the customer's message.
2. Identify and respond to each specific question or concern mentioned.
3. Use bullet points or short paragraphs to address each point.
4. Be polite, professional, and clear.
5. Close the email by inviting the customer to a meeting or to reach out with any further questions.

--- Output Format ---
Write the full email in English, starting with "Dear [Customer Name]" and ending with a proper sign-off.
""".strip()
    if debug:
        print("\n🧩 [Prompt 构造完成]")
        print(prompt)
        print("=" * 60)

    return prompt.strip()

