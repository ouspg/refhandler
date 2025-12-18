"""
Setup for the main FastAPI application
- CORS
- Combine API routes into one router with /api/ prefix
- Define /healthcheck endpoint and filter it from the logs
- Define lifespan for the app, used to initialize the database on startup
- Disable /docs, /redoc and /openapi.json if ENVIRONMENT was set to "production"
"""

# pylint: disable=missing-function-docstring, missing-module-docstring
import os
import logging
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi import APIRouter
from starlette.middleware.cors import CORSMiddleware

from backend.app.api.routes import login, users, pdfs
from backend.app.postgres_db import init_db_tables, create_default_admin

BACKEND_PORT = int(os.environ["BACKEND_PORT"])
FRONTEND_PORT = int(os.environ["FRONTEND_PORT"])
FRONTEND_HTTPS_PORT = int(os.environ["FRONTEND_HTTPS_PORT"])
ENVIRONMENT = os.environ["ENVIRONMENT"]

CORS_ALLOWED_ORIGINS = [
    "http://localhost",
    "http://127.0.0.1",
    f"http://localhost:{FRONTEND_PORT}",
    f"http://127.0.0.1:{FRONTEND_PORT}",
    f"https://localhost:{FRONTEND_HTTPS_PORT}",
    f"https://127.0.0.1:{FRONTEND_HTTPS_PORT}",
]

EXTRA_ALLOWED_ORIGIN_PORTS = os.environ.get("EXTRA_ALLOWED_ORIGIN_PORTS", "")  # Extra port for Development purpose, comma separated
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


# Define healthcheck endpoint
@api_router.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

# Filter healthcheck from uvicorn logs
class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return 'GET /api/healthcheck' not in record.getMessage()
logging.getLogger("uvicorn.access").addFilter(EndpointFilter())


# Initialize app
if ENVIRONMENT == "production":
    # Disables Swagger UI
    app = FastAPI(docs_url=None,
                redoc_url=None,
                openapi_url=None)
else:
    app = FastAPI(docs_url='/api/docs',
                redoc_url='/api/redoc',
                openapi_url='/api/openapi.json')

# include api router with /api prefix
app.include_router(api_router, prefix="/api")

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
