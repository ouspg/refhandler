import uvicorn
import requests
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from os import environ

TEST_FRONTEND_PORT = int(environ.get("TEST_FRONTEND_PORT", 'NO TEST_FRONTEND_PORT IN ENVIRONMENT'))
BACKEND_URL = f"http://backend:{environ.get("BACKEND_PORT")}"

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def serve_website():
    data = """
    <!DOCTYPE html>
<html>
<body>

<h1>Test frontend for testing Refhandler backend containers</h1>

<h2>Send text to the database</h2>

<form method="post" action="/add_post">
  <label for="db_text">Input your text here:</label><br>
  <input type="text" id="db_text" name="db_text" value="Hello World"><br><br>
  <input type="submit" value="Submit">
</form>

<h2>Upload a PDF file</h2>

<form method="post" action="/upload_pdf" enctype="multipart/form-data">
  <input type="file" name="pdf_file" accept="application/pdf"><br><br>
  <input type="submit" value="Upload">
</form>

</body>
</html>
    """

    return HTMLResponse(content=data, status_code=200)

@app.post("/add_post")
def add_post_to_database(db_text: str = Form()):
    res = requests.post(BACKEND_URL+"/add_post", json={"db_text": f"{db_text}"})
    return res.json()

@app.post("/upload_pdf")
async def upload_file(pdf_file: UploadFile = File()):
    files = {
        'pdf_file': (pdf_file.filename, await pdf_file.read(), pdf_file.content_type)
    }
    res = requests.post(BACKEND_URL+"/upload_pdf", files=files)
    return res.json()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=TEST_FRONTEND_PORT)