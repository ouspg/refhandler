from fastapi.testclient import TestClient

def test_post(client: TestClient):
    with open("backend/tests/api/test.pdf", "rb") as pdf_file:
        response = client.post("/api/pdfs", files={'pdf_file': pdf_file})
        data = response.json()
        assert response.status_code == 200
        assert data["original_filename"] == "test.pdf"
        assert data["uploaded_by"] == None
        
def test_post_with_missing_data(client: TestClient):
        response = client.post("/api/pdfs", files={'pdf_file': ""})
        assert response.status_code == 422
        
        response = client.post("/api/pdfs")
        assert response.status_code == 422
        
        response = client.post("/api/pdfs", data={"test": "test"})
        assert response.status_code == 422