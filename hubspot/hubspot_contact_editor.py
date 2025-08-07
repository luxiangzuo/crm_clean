# filename: hubspot_contact_editor.py

import requests
from hubspot.hubspot_oauth_server import get_valid_access_token

def update_contact_fields(contact_id: str, properties: dict):
    access_token = get_valid_access_token()

    url = f"https://api.hubapi.com/crm/v3/objects/contacts/{contact_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "properties": properties
    }

    response = requests.patch(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise RuntimeError(f"更新联系人失败: {response.text}")

    return response.json()
