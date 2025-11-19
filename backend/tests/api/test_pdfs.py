from fastapi.testclient import TestClient

def test_post(client: TestClient):
    with open("backend/tests/api/test.pdf", "rb") as pdf_file:
        # Upload test pdf file
        response_post = client.post("/api/pdfs", files={'pdf_file': pdf_file})
        data = response_post.json()
        assert response_post.status_code == 200
        assert data["original_filename"] == "test.pdf"
        assert data["uploaded_by"] == None
        
        # Get uploaded test file from backend and compare contents with original
        response_get = client.get(f"api/pdfs/{data["id"]}")
        pdf_file.seek(0)
        assert pdf_file.read() == response_get.content
        assert response_get.headers["content-type"] == "application/pdf"
        
        # remove uploaded test file
        response_delete = client.delete(f"api/pdfs/{data["id"]}")
        assert response_delete.status_code == 200
        
        # Make sure file was removed
        response_after_delete = client.get(f"api/pdfs/{data["id"]}")
        assert response_after_delete.status_code == 404


def test_post_with_missing_data(client: TestClient):
        response = client.post("/api/pdfs", files={'pdf_file': ""})
        assert response.status_code == 422
        
        response = client.post("/api/pdfs")
        assert response.status_code == 422
        
        response = client.post("/api/pdfs", data={"test": "test"})
        assert response.status_code == 422