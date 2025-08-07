# generate_prompt.py
"""
封装 prompt 模板，用于指导模型分类邮件（含边界判断、格式标准）
"""
def generate_prompt(email):
    return f"""
You are an expert CRM assistant.

Your task is to analyze the following email (including sender, subject and body) and extract:

1. **Sender's intent** in 5-10 words (in English)
2. **Customer stage**, selected from the options below:

[
  "None",              // Not related to business at all, or spam
  "Lead",              // Initial inquiry, general interest, vague contact
  "Qualified Lead",    // Expressed clear needs or asked for price/details
  "Opportunity",       // Specific opportunity: budget, timeline, proposal
  "Negotiation",       // Active back-and-forth, deal forming
  "Customer"           // Already purchased, existing client
]

%% If the email is irrelevant to business (e.g., spam, personal greeting, system notification), use `stage: None`.

%% If you're unsure or the email has no content, set `intent: \"unclear\"` and `stage: \"None\"`.

Return only this JSON structure (no explanation):

{{
  "intent": "...",
  "stage": "..."
}}

Now analyze:

From: {email['from']}
Subject: {email['subject']}
Body:
{email['body'][:1000]}
""".strip()
