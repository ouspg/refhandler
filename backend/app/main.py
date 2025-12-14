# pylint: disable=missing-function-docstring, missing-module-docstring
import os
import uvicorn
from fastapi import FastAPI
from fastapi import APIRouter
from starlette.middleware.cors import CORSMiddleware

from backend.app.api.routes import login, users, pdfs
from backend.app.db import init_db

BACKEND_PORT = int(os.environ.get("BACKEND_PORT", 'NO BACKEND_PORT IN ENVIRONMENT'))
FRONTEND_PORT = int(os.environ.get("FRONTEND_PORT", 'NO BACKEND_PORT IN ENVIRONMENT'))
ENVIRONMENT = os.environ.get("ENVIRONMENT", 'NO ENVIRONMENT IN ENVIRONMENT')

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


# Combine all routers into one API router
api_router = APIRouter()
api_router.include_router(pdfs.router, prefix="/pdfs", tags=["Pdfs"])
api_router.include_router(login.router, prefix="/login", tags=["Login"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])

# Initialize app and include api router with /api prefix
if ENVIRONMENT == "production":
    # Disables Swagger UI
    app = FastAPI(docs_url=None,
                redoc_url=None,
                openapi_url=None)
else:
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
    # TODO: get mutliple workers working. Integration tests fail 502 bad gateway
    uvicorn.run("main:app", host="0.0.0.0", port=BACKEND_PORT)
