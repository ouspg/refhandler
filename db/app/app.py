import uvicorn
import json
import sqlite3
from fastapi import FastAPI, Form, Request


app = FastAPI()


################################
# Database functions
################################
DB = "/var/lib/sqlite/test.db"

def execute_query(query: str):
    with sqlite3.connect(DB) as con:
        print(f"Executing query: [{query}]")
        cur = con.cursor()
        ret = cur.execute(query)
        con.commit()
        
        return ret

def initialize_db():
    query = """
    CREATE TABLE IF NOT EXISTS Posts(
	id INTEGER PRIMARY KEY,
    data TEXT
	);
    """
    
    print("initializing db")
    execute_query(query)

def add_post(text: str):
    query = f"""
    INSERT into Posts (data) VALUES ("{text}");
    """
    execute_query(query)

def get_all_posts():
    query = """
    SELECT * FROM Posts;
    """
    res = execute_query(query)
    return  json.dumps(res.fetchall())

##########################
# FastAPI edpoint handlers
##########################

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
