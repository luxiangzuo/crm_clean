# hubspot_notes_writer.py
import requests
import os
import json
from fastapi import APIRouter, HTTPException, Request
from hubspot.hubspot_oauth_server import get_valid_access_token
from hubspot.hubspot_contact_tools import get_contact_id_by_email
from datetime import datetime

router = APIRouter()

def write_note(contact_id: str, note_content: str, timestamp: int):
    access_token = get_valid_access_token()
    url = "https://api.hubapi.com/crm/v3/objects/notes"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "properties": {
            "hs_note_body": note_content,
            "hs_timestamp": timestamp
        },
        "associations": [
            {
                "to": {
                    "id": contact_id
                },
                "types": [
                    {
                        "associationCategory": "HUBSPOT_DEFINED",
                        "associationTypeId": 202
                    }
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 201:
        raise RuntimeError(f"❌ Note 写入失败: {response.text}")
    return response.json()

@router.post("/upload-notes-by-email")
async def upload_notes_by_email(request: Request):
    """
    输入 JSON 格式：
    [
        {
            "email": "client1@example.com",
            "notes": [
                {
                    "content": "邮件内容1",
                    "timestamp": "2025-07-29T11:00:00Z"
                },
                ...
            ]
        }
    ]
    """
    data = await request.json()
    success = []
    failed = []

    for entry in data:
        email = entry.get("email")
        notes = entry.get("notes", [])

        if not email or not notes:
            failed.append({"email": email, "reason": "缺少 email 或 notes"})
            continue

        contact_id = get_contact_id_by_email(email)
        if not contact_id:
            failed.append({"email": email, "reason": "未找到联系人"})
            continue

        for note in notes:
            try:
                note_content = note["content"]
                timestamp_str = note.get("timestamp")
                if not timestamp_str:
                    raise ValueError("❌ 缺少 timestamp 字段")

                timestamp = int(datetime.fromisoformat(timestamp_str.replace("Z", "+00:00")).timestamp() * 1000)
                write_note(contact_id, note_content, timestamp)

            except Exception as e:
                failed.append({"email": email, "reason": f"写入失败: {str(e)}"})
                break

        success.append(email)

    return {
        "msg": "批量写入完成",
        "success": success,
        "failed": failed
    }
