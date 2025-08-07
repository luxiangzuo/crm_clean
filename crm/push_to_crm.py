import json
import requests
from pathlib import Path
from dotenv import load_dotenv
import config
from requests.auth import HTTPBasicAuth
import re
from datetime import date
from email.utils import parseaddr

def is_valid_email(email: str) -> bool:
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

def extract_email_address(raw: str) -> str:
    return parseaddr(raw)[1].strip()

def sanitize_name(name: str) -> str:
    return re.sub(r'[^a-zA-Z0-9_\- ]', '', name)[:50] or "Anonymous"

load_dotenv()
EMAIL_FILE = "data/emails_classified.jsonl"

def read_emails(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return [json.loads(line.strip()) for line in f if line.strip()]

def get_auth():
    username = config.ESPOTCRM_USERNAME
    password = config.ESPOTCRM_PASSWORD
    if not username or not password:
        raise ValueError("❌ 环境变量未正确加载：ESPOTCRM_USERNAME 或 ESPOTCRM_PASSWORD 缺失")
    return HTTPBasicAuth(username, password)

def push_to_lead(email):
    email_from = extract_email_address(email.get("from", ""))
    if not is_valid_email(email_from):
        print(f"⚠️ 忽略：无效邮箱地址 -> {email_from}")
        return

    stage = email.get("stage", "").strip()
    crm_stage_mapping = {
        "Lead": "New",
        "Qualified Lead": "Qualified"
    }
    crm_stage = crm_stage_mapping.get(stage, "New")

    data = {
        "firstName": sanitize_name(email_from.split("@")[0]),
        "lastName": "(Imported)",
        "emailAddress": email_from,
        "description": email.get("body", "")[:512],
        "source": "Email",
        "stage": crm_stage,
        "intent": email.get("intent")
    }
    return post_to_crm("Lead", data)

def push_to_opportunity(email):
    email_from = extract_email_address(email.get("from", ""))
    if not is_valid_email(email_from):
        print(f"⚠️ 忽略：无效邮箱地址 -> {email_from}")
        return

    stage = email.get("stage", "").strip()
    crm_stage_mapping = {
        "Opportunity": "Qualification",
        "Negotiation": "Negotiation",
        "Qualified Lead": "Qualification"
    }
    crm_stage = crm_stage_mapping.get(stage, "Qualification")

    data = {
        "name": email.get("subject", "No Subject"),
        "accountName": sanitize_name(email_from.split("@")[0]),
        "description": email.get("body", "")[:512],
        "stage": crm_stage,
        "source": "Email",
        "amount": 0,
        "closeDate": date.today().isoformat()
    }
    return post_to_crm("Opportunity", data)

def push_to_contact(email):
    email_from = extract_email_address(email.get("from", ""))
    if not is_valid_email(email_from):
        print(f"⚠️ 忽略：无效邮箱地址 -> {email_from}")
        return

    data = {
        "firstName": sanitize_name(email_from.split("@")[0]),
        "lastName": "(Customer)",
        "emailAddress": email_from,
        "description": email.get("body", "")[:512]
    }
    return post_to_crm("Contact", data)

def post_to_crm(entity, data):
    url = f"{config.ESPOTCRM_URL}/api/v1/{entity}"
    response = requests.post(url, json=data, auth=get_auth())
    if response.status_code in [200, 201]:
        print(f"✅ 导入成功: {entity} - {data.get('emailAddress') or data.get('name')}")
    else:
        print(f"❌ 导入失败: {entity} - {response.status_code}: {response.text}")

def sanitize_email(email_text):
    plain = re.sub(r"[*_#\-]{1,}", "", email_text)
    return plain[:1800]

def update_opportunity_note(opportunity_id, reply_text):
    from config import ESPOTCRM_URL
    from .push_to_crm import get_auth

    url = f"{ESPOTCRM_URL}/api/v1/Opportunity/{opportunity_id}"
    data = {"description": reply_text[:1000]}
    response = requests.patch(url, json=data, auth=get_auth())
    if response.status_code in [200, 204]:
        print(f"✅ 回信内容已更新至 CRM - Opportunity {opportunity_id}")
    else:
        print(f"❌ 更新失败: {response.status_code} - {response.text}")

def main():
    emails = read_emails(EMAIL_FILE)
    print(f"📦 共有 {len(emails)} 封邮件，准备分类导入 CRM...")

    stage_to_entity = {
        "Lead": "Lead",
        "Qualified Lead": "Lead",
        "Opportunity": "Opportunity",
        "Negotiation": "Opportunity",
        "Customer": "Contact",
        "None": None
    }

    for email in emails:
        raw_stage = email.get("stage", "").strip()
        entity = stage_to_entity.get(raw_stage)

        if entity == "Lead":
            push_to_lead(email)
        elif entity == "Opportunity":
            push_to_opportunity(email)
        elif entity == "Contact":
            push_to_contact(email)
        else:
            print(f"⚠️ 忽略：无效阶段（stage: {raw_stage}）")

if __name__ == "__main__":
    main()
