# 📄 文件路径: api/hubspot_contact_creator.py
from fastapi import APIRouter, Body
import requests, os, json
from hubspot.hubspot_oauth_server import get_valid_access_token

router = APIRouter()

@router.post("/hubspot/create_contact")
def create_contact(data: dict = Body(...)):
    """
    创建新的 HubSpot 联系人
    请求示例：
    {
        "firstname": "小红",
        "lastname": "Dubois",
        "email": "xiaohong@example.com",
        "phone": "1234567890",
        "hs_lead_status": "NEW"
    }
    """
    try:
        access_token = get_valid_access_token()
    except Exception as e:
        return {"error": "Token 获取失败", "detail": str(e)}

    url = "https://api.hubapi.com/crm/v3/objects/contacts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    properties = {key: val for key, val in data.items() if val is not None}
    payload = {"properties": properties}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 201:
        return {"error": "创建联系人失败", "detail": response.text}

    return {"✅ 联系人创建成功": response.json()}
