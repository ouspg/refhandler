from typing import Annotated
import uvicorn
from fastapi import FastAPI, Request, Depends, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
import os

DATABASE_URL = "postgresql://user:password@postgres:5432/refhandler"
engine = create_engine(DATABASE_URL)

UPLOAD_DIR = os.environ.get("UPLOAD_DIR", "/pdf_uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

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

@app.get("/", response_class=HTMLResponse)
def serve_upload_page():
    data = """
    <!DOCTYPE html>
<html>
<body>

<h2>Upload a PDF file</h2>

<form method=\"post\" action=\"/upload_pdf\" enctype=\"multipart/form-data\">
  <input type=\"file\" name=\"pdf_file\" accept=\"application/pdf\"><br><br>
  <input type=\"submit\" value=\"Upload\">
</form>

</body>
</html>
    """
    return HTMLResponse(content=data, status_code=200)

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
    uvicorn.run(app, host="0.0.0.0", port=8001)
