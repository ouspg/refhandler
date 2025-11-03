from fastapi import APIRouter
from sqlmodel import select
from app.api.deps import SessionDep
from app.models.models import Post

router = APIRouter(prefix="/posts")

@router.get("/")
def get_all_posts(session: SessionDep):
    posts = session.exec(select(Post)).all()
    return posts

@router.post("/")
def add_post(post: Post, session: SessionDep):
    session.add(post)
    session.commit()
    session.refresh(post)
    
    res = {"message": "Post added to database",
           "post": post,
           "Posts table after changes": get_all_posts(session)}
    return res