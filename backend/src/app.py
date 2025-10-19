from typing import Annotated
import uvicorn
from sqlmodel import Session, select
from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.responses import HTMLResponse
import os
from backend.src.db.models import Post
from backend.src.db.db import initialize_db, get_session

BACKEND_PORT = int(os.environ.get("BACKEND_PORT", 'NO BACKEND_PORT IN ENVIRONMENT'))
app = FastAPI()
SessionDep = Annotated[Session, Depends(get_session)]

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

UPLOAD_DIR = os.environ.get("UPLOAD_DIR", "/pdf_uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload_pdf")
async def upload_pdf(pdf_file: UploadFile = File()):
    print(pdf_file)
    if pdf_file.content_type != "application/pdf":
        return {"error": "Only PDF files are allowed."}
    file_location = os.path.join(UPLOAD_DIR, pdf_file.filename)
    with open(file_location, "wb") as f:
        f.write(pdf_file.file.read())
    return {"filename": pdf_file.filename, "message": "PDF uploaded successfully."}
    
if __name__ == "__main__":
    initialize_db()
    uvicorn.run(app, host="0.0.0.0", port=BACKEND_PORT)
