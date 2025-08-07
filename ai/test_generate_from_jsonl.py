# test_generate_from_jsonl.py
import json
from typing import Literal, cast
import sys
import os

# 将项目根目录加入 Python 模块查找路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 引入你原有模块
from utils.model_loader import call_model
from prompt.generate_sales_prompt import build_prompt
from rag.retrieve_docs import retrieve_docs
from generate_sales_reply import generate_sales_reply_from_email

# 定位数据路径
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/emails_classified.jsonl")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "../data/generated_replies.jsonl")

# 加载 JSONL 数据
with open(DATA_PATH, "r", encoding="utf-8") as f:
    lines = [json.loads(line.strip()) for line in f]

results = []

# 遍历每封邮件生成回复
for i, email in enumerate(lines):
    sender = email.get("from", "Client")
    name = sender.split('"')[1] if '"' in sender else sender.split("<")[0].strip()
    body = email.get("body", "")
    subject = email.get("subject", "")
    intent = email.get("intent", "")
    stage = email.get("stage", "")

    print(f"\n📨 [第{i+1}封邮件 - 来自 {name} | 意图: {intent} | 阶段: {stage}]\n主题: {subject}\n正文:\n{body}\n")

    reply = generate_sales_reply_from_email(name=name, email_text=body)
    print(f"\n✉️ [AI 回复建议]\n{reply}\n{'='*60}")

    results.append({
        "from": sender,
        "subject": subject,
        "body": body,
        "intent": intent,
        "stage": stage,
        "ai_reply": reply
    })

# 保存到新文件
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    for item in results:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"\n✅ 所有回复已生成并保存到：{OUTPUT_PATH}")
