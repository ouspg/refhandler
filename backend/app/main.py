import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import os
from app.db import initialize_db
from app.api.main import api_router

BACKEND_PORT = int(os.environ.get("BACKEND_PORT", 'NO BACKEND_PORT IN ENVIRONMENT'))
FRONTEND_PORT = int(os.environ.get("FRONTEND_PORT", 'NO BACKEND_PORT IN ENVIRONMENT'))

CORS_ALLOWED_ORIGINS = [
    "http://localhost",
    "http://127.0.0.1",
    f"http://localhost:{FRONTEND_PORT}",
    f"http://127.0.0.1:{FRONTEND_PORT}",
]

EXTRA_ALLOWED_ORIGIN_PORTS = os.environ.get("EXTRA_ALLOWED_ORIGIN_PORTS", '')  # Extra port for Development purpose, comma separated
EXTRA_ALLOWED_ORIGIN_PORTS = [
    p for p in (s.strip() for s in EXTRA_ALLOWED_ORIGIN_PORTS.split(','))
    if p.isdigit() and 1 <= int(p) <= 65535
]
for p in EXTRA_ALLOWED_ORIGIN_PORTS:
    CORS_ALLOWED_ORIGINS.extend([f"http://localhost:{p}", f"http://127.0.0.1:{p}"])

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
    initialize_db()
    uvicorn.run(app, host="0.0.0.0", port=BACKEND_PORT)
