import uvicorn
import json
from fastapi import FastAPI, Request
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgres:5432/refhandler"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    data = Column(String)

def initialize_db():
    Base.metadata.create_all(bind=engine)

app = FastAPI()
initialize_db()

def add_post(text: str):
    db = SessionLocal()
    post = Post(data=text)
    db.add(post)
    db.commit()
    db.refresh(post)
    db.close()

def get_all_posts():
    db = SessionLocal()
    posts = db.query(Post).all()
    db.close()
    return json.dumps([{"id": p.id, "data": p.data} for p in posts])

@app.get("/get_all_posts")
def handle_get_all_posts():
    return get_all_posts()

@app.post("/add_post")
async def handle_add_post(request: Request):
    post = await request.json()
    text = str(post["db_text"])
    add_post(text)
    
    res = {"message": "Post added to database",
           "Posts table after changes": get_all_posts()}
    return res
    
if __name__ == "__main__":
    initialize_db()
    uvicorn.run(app, host="0.0.0.0", port=8001)
