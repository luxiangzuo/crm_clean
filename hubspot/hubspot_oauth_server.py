# filename: hubspot_oauth_server.py

from fastapi import Request
import requests, os, json
from datetime import datetime, timedelta

CLIENT_ID = "6d980ab9-5759-42a1-a7d4-cab1caa5e74b"
CLIENT_SECRET = "b26c391d-7db2-45fd-b657-6449132f34bb"
REDIRECT_URI = "http://localhost:8000/hubspot/oauth/callback"
TOKEN_PATH = os.path.join("data", "token.json")


# ✅ 工具函数：自动判断过期并刷新
def get_valid_access_token():
    if not os.path.exists(TOKEN_PATH):
        raise RuntimeError("token.json 不存在，请先授权")

    with open(TOKEN_PATH, "r") as f:
        tokens = json.load(f)

    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")
    expires_in = tokens.get("expires_in", 1800)
    fetched_at_str = tokens.get("fetched_at")

    if not all([access_token, refresh_token, fetched_at_str]):
        raise RuntimeError("token.json 缺少字段")

    fetched_at = datetime.fromisoformat(fetched_at_str)
    expired_at = fetched_at + timedelta(seconds=expires_in)

    if datetime.utcnow() >= expired_at:
        print("🔄 Token 过期，自动刷新中...")
        token_url = "https://api.hubapi.com/oauth/v1/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "refresh_token",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": refresh_token,
        }
        resp = requests.post(token_url, headers=headers, data=data)
        if resp.status_code != 200:
            raise RuntimeError(f"刷新失败: {resp.text}")
        new_tokens = resp.json()
        new_tokens["fetched_at"] = datetime.utcnow().isoformat()
        with open(TOKEN_PATH, "w") as f:
            json.dump(new_tokens, f)
        return new_tokens["access_token"]

    return access_token


# ✅ 导出路由函数：在 app.py 中注册
async def hubspot_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "No code in URL"}

    token_url = "https://api.hubapi.com/oauth/v1/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": code
    }
    response = requests.post(token_url, headers=headers, data=data)
    if response.status_code != 200:
        return {"error": "Failed to get token", "detail": response.text}

    tokens = response.json()
    tokens["fetched_at"] = datetime.utcnow().isoformat()
    os.makedirs("data", exist_ok=True)
    with open(TOKEN_PATH, "w") as f:
        json.dump(tokens, f)

    return {"✅ Access token 获取成功！": tokens}


# ✅ 工具函数
def refresh_access_token_manual():
    if not os.path.exists(TOKEN_PATH):
        return {"error": "token.json 不存在"}

    with open(TOKEN_PATH, "r") as f:
        tokens = json.load(f)

    refresh_token = tokens.get("refresh_token")
    if not refresh_token:
        return {"error": "refresh_token 缺失"}

    token_url = "https://api.hubapi.com/oauth/v1/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": refresh_token,
    }

    response = requests.post(token_url, headers=headers, data=data)
    if response.status_code != 200:
        return {"error": "Failed to refresh token", "detail": response.text}

    new_tokens = response.json()
    new_tokens["fetched_at"] = datetime.utcnow().isoformat()

    with open(TOKEN_PATH, "w") as f:
        json.dump(new_tokens, f)

    return {"✅ Token 刷新成功": new_tokens}




# 核心职责是：

# 管理 OAuth token 的生命周期（初次获取、刷新、存储）

# 提供 get_valid_access_token() 工具函数供其他模块使用

# 提供 /hubspot/oauth/callback FastAPI 路由接收授权码并换取 token