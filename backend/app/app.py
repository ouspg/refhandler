from typing import Annotated
import uvicorn
from fastapi import FastAPI, Request, Depends, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

DATABASE_URL = "postgresql://user:password@postgres:5432/refhandler"
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
initialize_db()


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
    uvicorn.run(app, host="0.0.0.0", port=8001)
