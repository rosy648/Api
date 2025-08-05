from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import uvicorn
import socket

app = FastAPI()

class LoginRequest(BaseModel):
    email: str
    password: str

LOGIN_URL = "https://discord.com/api/v9/auth/login"

@app.post("/login")
async def login(data: LoginRequest):
    payload = {
        "login": data.email,
        "password": data.password,
        "undelete": False,
        "captcha_key": None,
        "login_source": None,
        "gift_code_sku_id": None
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(LOGIN_URL, json=payload, headers=headers)

    if response.status_code == 200:
        json_data = response.json()
        token = json_data.get("token")
        if token:
            return {"status": "success", "token": token}
        else:
            raise HTTPException(status_code=401, detail="Login สำเร็จแต่ไม่มี token (อาจมี CAPTCHA หรือ 2FA)")
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Login ผิดพลาด: {response.text}")

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

if __name__ == "__main__":
    port = 8080
    local_ip = get_local_ip()

    print("🚀 API Running!")
    print(f" - Localhost: http://127.0.0.1:{port}/docs")
    print(f" - LAN IP: http://{local_ip}:{port}/docs")
    print(" - (ถ้าอยู่บน Replit ให้ใช้ URL ที่ Replit ให้มา)")

    uvicorn.run(app, host="0.0.0.0", port=port)
