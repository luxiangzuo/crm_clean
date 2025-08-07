# pull_from_crm.py
import requests
from config import ESPOTCRM_URL
from crm.push_to_crm import get_auth


def pull_from_crm(opportunity_id):
    """
    根据机会ID从 CRM 获取 Opportunity 数据。
    """
    url = f"{ESPOTCRM_URL}/api/v1/Opportunity/{opportunity_id}"
    response = requests.get(url, auth=get_auth())
    if response.status_code == 200:
        print(f"📥 成功获取 Opportunity 数据 - ID: {opportunity_id}")
        return response.json()
    else:
        print(f"❌ 拉取失败: {response.status_code} - {response.text}")
        return None