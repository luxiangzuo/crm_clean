from fastapi import APIRouter, Body
from ai.generate_sales_reply import generate_sales_reply_from_email

router = APIRouter()

@router.post("/ai/generate_reply")
def generate_reply(data: dict = Body(...)):
    contact_id = data.get("contact_id")
    email = data.get("email")
    name = data.get("first_name", "there")

    if not contact_id or not email:
        return {"error": "缺少 contact_id 或 email"}

    try:
        reply = generate_sales_reply_from_email(name, email)
        return {"reply": reply}
    except Exception as e:
        return {"error": "生成内容失败", "detail": str(e)}
