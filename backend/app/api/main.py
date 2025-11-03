from fastapi import APIRouter
from app.api.routes import pdfs, posts

api_router = APIRouter()
api_router.include_router(pdfs.router)
api_router.include_router(posts.router)