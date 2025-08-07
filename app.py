# app.py
from fastapi import FastAPI
from ai.router import router as ai_router
from hubspot.hubspot_oauth_server import hubspot_callback
from hubspot.hubspot_contact_tools import router as contact_tools_router
from hubspot.router import router as hubspot_router  # ✅ 加这一行！
from hubspot.hubspot_notes_writer import router as hubspot_router


app = FastAPI()
print("📌 正在注册 HubSpot contact_tools_router ...")
app.include_router(contact_tools_router)
app.include_router(hubspot_router)  # ✅ 加这一行！
app.include_router(ai_router)

app.add_api_route("/hubspot/oauth/callback", hubspot_callback, methods=["GET"])

@app.on_event("startup")
async def show_routes():
    print("📋 当前 FastAPI 注册的所有路径：")
    for route in app.routes:
        print(f"{route.path} → {route.name}")
