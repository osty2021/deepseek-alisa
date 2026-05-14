import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/")
async def main(request: Request):
    return JSONResponse({
        "response": {
            "text": "Привет! Сервер работает.",
            "end_session": False
        },
        "version": "1.0"
    })
