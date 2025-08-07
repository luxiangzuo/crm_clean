# filename: hubspot_contact_tools.py

from fastapi import APIRouter
import requests
from .hubspot_oauth_server import get_valid_access_token

import requests
from hubspot.hubspot_oauth_server import get_valid_access_token
# ✅ 新增的 FastAPI 路由定义
from fastapi import Query
router = APIRouter()


def list_email_engagements(contact_id, limit=10):
    access_token = get_valid_access_token()

    url = f"https://api.hubapi.com/engagements/v1/engagements/associated/contact/{contact_id}/paged"
    headers = {"Authorization": f"Bearer {access_token}"}

    results = []
    has_more = True
    offset = 0

    while has_more and len(results) < limit:
        params = {"limit": 100, "offset": offset}
        resp = requests.get(url, headers=headers, params=params)
        data = resp.json()

        engagements = data.get("results", [])
        for item in engagements:
            e = item.get("engagement", {})
            meta = item.get("metadata", {})
            if e.get("type") == "EMAIL":
                results.append({
                    "id": e.get("id"),
                    "timestamp": e.get("timestamp"),
                    "subject": meta.get("subject"),
                    "text": meta.get("text"),
                    "from": meta.get("from", {}).get("email"),
                    "to": meta.get("to", []),
                })

        has_more = data.get("hasMore", False)
        offset = data.get("offset", 0)

    return results[:limit]

def get_contact_id_by_email(email: str) -> str:
    access_token = get_valid_access_token()
    url = f"https://api.hubapi.com/crm/v3/objects/contacts/search"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    data = {
        "filterGroups": [{
            "filters": [{
                "propertyName": "email",
                "operator": "EQ",
                "value": email
            }]
        }],
        "properties": ["email"]
    }

    resp = requests.post(url, headers=headers, json=data)
    if resp.status_code != 200:
        raise RuntimeError(f"获取联系人失败: {resp.text}")

    results = resp.json().get("results", [])
    if not results:
        raise ValueError(f"找不到邮箱为 {email} 的联系人")

    return results[0]["id"]


# ✅ 1. 获取简化联系人列表
@router.get("/hubspot/list_contacts_simple")
def list_contacts_simple():
    try:
        access_token = get_valid_access_token()
    except Exception as e:
        return {"error": "token 获取失败", "detail": str(e)}

    url = "https://api.hubapi.com/crm/v3/objects/contacts"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return {"error": "获取联系人失败", "detail": resp.text}

    data = resp.json()
    simplified = []
    for item in data.get("results", []):
        props = item.get("properties", {})
        simplified.append({
            "id": item.get("id"),
            "email": props.get("email"),
            "firstname": props.get("firstname"),
            "lastname": props.get("lastname")
        })

    return {"contacts": simplified}


# ✅ 2. 获取当前 token 的 scopes
@router.get("/hubspot/get_token_scopes")
def get_token_scopes():
    try:
        access_token = get_valid_access_token()
    except Exception as e:
        return {"error": "token 获取失败", "detail": str(e)}

    url = "https://api.hubapi.com/oauth/v1/access-tokens/" + access_token
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return {"error": "获取 scopes 失败", "detail": resp.text}

    return resp.json()


# ✅ 3. 列出联系人所有字段（标准 + 自定义）
@router.get("/hubspot/list_contact_fields")
def list_contact_fields():
    try:
        access_token = get_valid_access_token()
    except Exception as e:
        return {"error": "token 获取失败", "detail": str(e)}

    url = "https://api.hubapi.com/crm/v3/properties/contacts"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return {"error": "获取字段失败", "detail": resp.text}

    results = resp.json().get("results", [])
    return [
        {
            "name": prop.get("name"),
            "label": prop.get("label"),
            "fieldType": prop.get("fieldType"),
            "type": prop.get("type")
        }
        for prop in results
    ]



@router.get("/hubspot/list_contacts_simple")
def list_contacts_simple_route():
    return list_contacts_simple()

@router.get("/hubspot/get_token_scopes")
def get_token_scopes_route():
    return get_token_scopes()

@router.get("/hubspot/list_contact_fields")
def list_contact_fields_route():
    return list_contact_fields()





#核心职责是：使用 token 发起各种 HubSpot API 调用提供路由接口如：
#/hubspot/list_contacts_simple/hubspot/get_token_scopes/hubspot/list_contact_fields
#并且所有接口都依赖 get_valid_access_token() 来隐式完成授权流程 ✅