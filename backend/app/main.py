from typing import Annotated
import uvicorn
from sqlmodel import Session, select
from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware
import os
from app.models.models import Post
from app.db import initialize_db, get_session
from app.api.main import api_router

BACKEND_PORT = int(os.environ.get("BACKEND_PORT", 'NO BACKEND_PORT IN ENVIRONMENT'))
FRONTEND_PORT = int(os.environ.get("FRONTEND_PORT", 'NO BACKEND_PORT IN ENVIRONMENT'))
CORS_ALLOWED_ORIGINS = [
    "http://localhost",
    f"http://localhost:{FRONTEND_PORT}",
]


app = FastAPI()
app.include_router(api_router, prefix="/api")

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    initialize_db()
    uvicorn.run(app, host="0.0.0.0", port=BACKEND_PORT)
