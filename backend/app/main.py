import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import os
from fastapi import APIRouter
from app.api.routes import pdfs
from app.db import init_db

BACKEND_PORT = int(os.environ.get("BACKEND_PORT", 'NO BACKEND_PORT IN ENVIRONMENT'))
FRONTEND_PORT = int(os.environ.get("FRONTEND_PORT", 'NO BACKEND_PORT IN ENVIRONMENT'))
CORS_ALLOWED_ORIGINS = [
    "http://localhost",
    f"http://localhost:{FRONTEND_PORT}",
]

# Combine all routers into one API router
api_router = APIRouter()
api_router.include_router(pdfs.router, prefix="/pdfs", tags=["Pdfs"])

# Initialize app and include api router with /api prefix
app = FastAPI(docs_url='/api/docs', 
                redoc_url='/api/redoc',
                openapi_url='/api/openapi.json')
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
    init_db()
    uvicorn.run(app, host="0.0.0.0", port=BACKEND_PORT)
