import uvicorn
import requests
from fastapi import FastAPI
from fastapi.responses import RedirectResponse


app = FastAPI()

@app.get("/")
def handle_redirect():
    return RedirectResponse(url=f"/all_visits", status_code=303)

@app.get("/all_visits")
def handle_all_visits():
    res = requests.get("http://db:8001/all_visits")
    return res.json()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)