from fastapi.testclient import TestClient

def test_post(client: TestClient):  
    db_text = "hello world"
    response = client.post( "/api/posts", json={"db_text": db_text})
    
    data = response.json()
    assert response.status_code == 200
    
def test_get(client: TestClient):
    db_text = "hello world"
    response = client.post( "/api/posts", json={"db_text": db_text})
    response = client.post( "/api/posts", json={"db_text": db_text})
    
    response = client.get("/api/posts")
    data = response.json()
    
    assert response.status_code == 200
    assert data == [{'id': 1, 'db_text': 'hello world'}, {'id': 2, 'db_text': 'hello world'}]