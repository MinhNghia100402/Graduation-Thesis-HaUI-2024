import os, json
from fastapi import FastAPI
from fastapi import Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import uvicorn
from ratelimit import RateLimitMiddleware, Rule
from ratelimit.types import Scope
from ratelimit.backends.simple import MemoryBackend

from src.routers import chat

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat.router, prefix="", tags=["chat"])

def main():
    uvicorn.run(app, host="0.0.0.0", port=9999)

if __name__ == "__main__":
    main()
