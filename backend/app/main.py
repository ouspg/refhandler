from typing import Annotated
import uvicorn
from sqlmodel import Session, select
from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.responses import HTMLResponse
import os
from app.models.models import Post
from app.db import initialize_db, get_session
from app.api.main import api_router

BACKEND_PORT = int(os.environ.get("BACKEND_PORT", 'NO BACKEND_PORT IN ENVIRONMENT'))
app = FastAPI()
app.include_router(api_router)

if __name__ == "__main__":
    initialize_db()
    uvicorn.run(app, host="0.0.0.0", port=BACKEND_PORT)
