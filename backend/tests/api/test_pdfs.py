from fastapi.testclient import TestClient

def test_post(client: TestClient):
    with open("backend/tests/api/test.pdf", "rb") as pdf_file:
        response = client.post("/api/pdfs", files={'files': pdf_file})
        data = response.json()
        assert response.status_code == 200
        for file in data:
            assert file["original_filename"] == "test.pdf"
            assert file["uploaded_by"] == None

def test_post_multiple_files(client: TestClient):
    with open("backend/tests/api/test.pdf", "rb") as pdf_file1,\
            open("backend/tests/api/test.pdf", "rb") as pdf_file2:
        files = [('files', pdf_file1), ('files', pdf_file2)]
        
        response = client.post("/api/pdfs", files=files)
        data = response.json()
        assert response.status_code == 200
        for file in data:
            assert file["original_filename"] == "test.pdf"
            assert file["uploaded_by"] == None
        
def test_post_with_missing_data(client: TestClient):
        response = client.post("/api/pdfs", files={'pdf_file': ""})
        assert response.status_code == 422
        
        response = client.post("/api/pdfs")
        assert response.status_code == 422
        
        response = client.post("/api/pdfs", data={"test": "test"})
        assert response.status_code == 422