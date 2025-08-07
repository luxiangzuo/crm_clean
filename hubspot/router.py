from fastapi import APIRouter, Body
from hubspot.hubspot_contact_creator import create_contact
from hubspot.hubspot_contact_editor import update_contact_fields
from hubspot.hubspot_notes_writer import write_note
from hubspot.hubspot_oauth_server import hubspot_callback
from hubspot.hubspot_contact_tools import list_email_engagements
from hubspot.hubspot_contact_tools import get_contact_id_by_email

router = APIRouter()


@router.post("/hubspot/create_contact")
def create(data: dict = Body(...)):
    return create_contact(data)

@router.patch("/hubspot/update_contact")
def update(data: dict = Body(...)):
    contact_id = data.get("contact_id")
    properties = data.get("properties")

    if not contact_id or not isinstance(properties, dict):
        return {"error": "缺少 contact_id 或属性不合法"}
    return update_contact_fields(contact_id, properties)

@router.post("/hubspot/write_note")
def write(data: dict = Body(...)):
    contact_id = data.get("contact_id")
    note = data.get("note")
    return write_note(contact_id, note)

@router.post("/hubspot/ai_followup_note")
def ai_followup(data: dict = Body(...)):
    from ai.generate_sales_reply import generate_sales_reply_from_email
    contact_id = data.get("contact_id")
    email = data.get("email")
    name = data.get("first_name", "there")

    if not contact_id or not email:
        return {"error": "缺少 contact_id 或 email"}

    try:
        reply = generate_sales_reply_from_email(name, email)
        return write_note(contact_id, reply)
    except Exception as e:
        return {"error": "AI 生成或写入失败", "detail": str(e)}

@router.get("/hubspot/oauth/callback")
async def callback(request):
    return await hubspot_callback(request)

@router.get("/hubspot/list_email_engagements")
def get_engagements(contact_id: str):
    try:
        emails = list_email_engagements(contact_id)
        return {"emails": emails}
    except Exception as e:
        return {"error": str(e)}

@router.post("/write_notes_by_email")
def write_notes_by_email(email: str, notes: list[str]):
    try:
        contact_id = get_contact_id_by_email(email)
    except Exception as e:
        return {"error": f"查找联系人失败: {str(e)}"}

    results = []
    for note in notes:
        try:
            res = write_note(contact_id, note)
            results.append(res)
        except Exception as e:
            results.append({"error": str(e), "note": note})

    return {"msg": "写入完成", "results": results}


