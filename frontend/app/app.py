import uvicorn
import requests
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse


app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def serve_website():
    data = """
    <!DOCTYPE html>
<html>
<body>

<h2>Send text to the database</h2>

<form method="post" action="/add_post">
  <label for="db_text">Input your text here:</label><br>
  <input type="text" id="db_text" name="db_text" value="Hello World"><br><br>
  <input type="submit" value="Submit">
</form>

</body>
</html>
    """

    return HTMLResponse(content=data, status_code=200)

@app.post("/add_post")
def add_post_to_database(db_text: str = Form()):
    res = requests.post("http://db:8001/add_post/", json={"db_text": f"{db_text}"})
    return res.json()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)