import uvicorn
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
import os

UPLOAD_DIR = "/pdf_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()

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
    contents = await pdf_file.read()
    print(pdf_file)
    if pdf_file.content_type != "application/pdf":
        return {"error": "Only PDF files are allowed."}
    file_location = os.path.join(UPLOAD_DIR, pdf_file.filename)
    with open(file_location, "wb") as f:
        f.write(pdf_file.file.read())
    return {"filename": pdf_file.filename, "message": "PDF uploaded successfully."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
