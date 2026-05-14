import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.vsegpt.ru/v1")
MODEL = os.getenv("DEEPSEEK_MODEL", "openai/gpt-3.5-turbo")

@app.post("/")
async def main(request: Request):
    try:
        req = await request.json()
        command = req.get("request", {}).get("command", "")
        if not command:
            command = req.get("request", {}).get("original_utterance", "")
        if not command:
            command = "Привет"

        response = requests.post(
            f"{BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": "Ты — полезный ассистент по имени DeepSeek. Отвечай по-русски."},
                    {"role": "user", "content": command}
                ]
            },
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            answer = data["choices"][0]["message"]["content"]
        else:
            answer = f"Ошибка API: {response.status_code}"

        return JSONResponse({
            "response": {
                "text": answer,
                "end_session": False
            },
            "version": "1.0"
        })

    except Exception as e:
        return JSONResponse({
            "response": {
                "text": f"Внутренняя ошибка: {e}",
                "end_session": False
            },
            "version": "1.0"
        })
