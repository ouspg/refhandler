import uvicorn
import json
import sqlite3
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

################################
# Database functions
################################
DB = "/var/lib/sqlite/test.db"

def execute_query(query: str):
    with sqlite3.connect(DB) as con:
        cur = con.cursor()
        ret = cur.execute(query)
        con.commit()
        
        return ret

def initialize_db():
    query = """
    CREATE TABLE IF NOT EXISTS Visits(
	visit_time DATETIME NOT NULL
	);
    """
    execute_query(query)

def add_visit():
    query = """
    INSERT into Visits VALUES (CURRENT_TIMESTAMP);
    """
    execute_query(query)

def get_all_visits():
    query = """
    SELECT * FROM Visits;
    """
    res = execute_query(query)
    return  json.dumps(res.fetchall())

def get_last_visit():
    query = """
    SELECT MAX(Visits.visit_time) FROM Visits;
    """
    res = execute_query(query)
    return  json.dumps({"Last visit": res.fetchall()})

##########################
# FastAPI edpoint handlers
##########################
app = FastAPI()

@app.get("/")
def handle_redirect():
    return RedirectResponse(url=f"/all_visits", status_code=303)

@app.get("/all_visits")
def handle_all_visits():
    add_visit()
    return get_all_visits()

@app.get("/last_visit")
def handle_last_visit():
    add_visit()
    return get_last_visit()

if __name__ == "__main__":
    initialize_db()
    
    uvicorn.run(app, host="0.0.0.0", port=8001)