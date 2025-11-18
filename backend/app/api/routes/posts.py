from fastapi import APIRouter
from sqlmodel import select
from app.api.depdendancies import SessionDep
from app.models import Post, PostCreate, PostPublic

router = APIRouter()

@router.get("/")
def get_all_posts(session: SessionDep):
    posts = session.exec(select(Post)).all()
    return posts

@router.post("/")
def add_post(post: PostCreate, session: SessionDep):
    db_post = Post.model_validate(post)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    
    res = {"message": "Post added to database",
           "post": db_post,
           "Posts table after changes": get_all_posts(session)}
    return res