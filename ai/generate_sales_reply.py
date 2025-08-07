# ai/generate_sales_reply.py
# python -m ai.generate_sales_reply
from utils.model_loader import call_model
from prompt.generate_sales_prompt import build_prompt
import json
from typing import Literal, cast
from pathlib import Path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def generate_sales_reply_from_email(name: str, email_text: str, model: str = "openai", debug: bool = False) -> str:
    """
    通过客户姓名与邮件正文生成销售回信。
    debug=True 时会打印 prompt 与检索信息，方便分析。
    """
    customer_info = {
        "name": name,
        "stage": "Unknown",
        "product": "Unknown"
    }

    email_summary = {
    "主题": email.get("subject", ""),
    "正文": email.get("body", "")
    }


    # build_prompt 会内部调用 retrieve_docs 并打印调试信息（如果开启 debug）
    prompt = build_prompt(customer_info, email_summary, debug=debug)

    reply = call_model(prompt, model_name=cast(Literal["openai", "gemini"], model))

    if debug:
        print("\n✉️ [模型生成的 AI 回信]")
        print(reply)
        print("=" * 60)

    return reply


if __name__ == "__main__":
    from pathlib import Path

    BASE_DIR = Path(__file__).resolve().parent.parent
    GMAIL_DIR = BASE_DIR / "data" / "gmail"
    INPUT_FILE = GMAIL_DIR / "emails_classified.jsonl"

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = [json.loads(line.strip()) for line in f]

    for i, email in enumerate(lines[:3]):
        sender = email.get("from", "Client")
        name = sender.split('"')[1] if '"' in sender else sender.split("<")[0].strip()
        body = email.get("body", "")

        print(f"\n📨 [第{i+1}封邮件 - 来自 {name}]\n{body}\n")
        reply = generate_sales_reply_from_email(name=name, email_text=body, debug=True)
        print(f"\n✅ 生成完成 ✅\n{'='*60}")
