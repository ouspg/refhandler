from typing import Annotated
import uvicorn
from fastapi import FastAPI, Request, Depends, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from pydantic import PostgresDsn
from os import environ

BACKEND_PORT = int(environ.get("BACKEND_PORT", 'NO BACKEND_PORT IN ENVIRONMENT'))
POSTGRES_USER = environ.get("POSTGRES_USER", 'NO POSTGRES_USER IN ENVIRONMENT')
POSTGRES_PASSWORD = environ.get("POSTGRES_PASSWORD", 'NO POSTGRES_PASSWORD IN ENVIRONMENT')
POSTGRES_DB = environ.get("POSTGRES_DB", 'NO POSTGRES_DB IN ENVIRONMENT')
POSTGRES_SERVER = environ.get("POSTGRES_SERVER", 'NO POSTGRES_SERVER IN ENVIRONMENT')
POSTGRES_PORT = environ.get("POSTGRES_PORT", 'NO POSTGRES_PORT IN ENVIRONMENT')
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL)

class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    db_text: str

def initialize_db():
    SQLModel.metadata.create_all(bind=engine)
    
def get_session():
    with Session(engine) as session:
        yield session
    
SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI()


@app.get("/get_all_posts")
def get_all_posts(session: SessionDep):
    posts = session.exec(select(Post)).all()
    return posts

@app.post("/add_post")
def add_post(post: Post, session: SessionDep):
    session.add(post)
    session.commit()
    session.refresh(post)
    
    res = {"message": "Post added to database",
           "Posts table after changes": get_all_posts(session)}
    return res
    
if __name__ == "__main__":
    initialize_db()
    uvicorn.run(app, host="0.0.0.0", port=BACKEND_PORT)
