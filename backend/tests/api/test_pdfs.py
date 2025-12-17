"""
Unit tests for /api/pdfs
"""
# pylint: disable=missing-function-docstring
from fastapi.testclient import TestClient
from httpx import Response
from sqlmodel import Session
from backend.app.models import UserCreate, UserRole, PdfPublic, PdfUpdate
from backend.app.api import user_crud


test_email = "foo@bar.com"
test_password = "foobarbaz"
test_user = UserCreate(email=test_email, password=test_password)

test_admin = UserCreate(role=UserRole.admin,
                        email="admin@admin.com", password=test_password)

def _get_oauth2_login(username: str, password: str):
    return {"username": username, "password": password }

def _get_access_token(client: TestClient, username: str, password: str):
    login = _get_oauth2_login(username, password)
    response_token = client.post("/api/login/access-token", data=login)
    return response_token.json()

def _get_access_token_header(client: TestClient, username: str, password: str):
    token = _get_access_token(client, username, password)
    return {"Authorization": f"Bearer {token}"}

def test_post_get_patch_delete(session: Session, client: TestClient, mocker):
    created_user = user_crud.create_user(session, test_user)
    assert created_user is not None
    token_header = _get_access_token_header(client, test_email, test_password)

    # Mock scanner results for a safe file
    mocker.patch("backend.app.api.scanners.Scanners.clamav_scan",
                 return_value=Response(200, json={"results": "foobar"}))
    mocker.patch("backend.app.api.scanners.Scanners.virustotal_scan",
                 return_value=Response(200, json={"results": "foobar"}))

    with open("backend/tests/api/test.pdf", "rb") as pdf_file:
        # Upload test pdf file
        files={'pdf_file': pdf_file}
        response_post = client.post("/api/pdfs", files=files, headers=token_header)
        db_pdf = PdfPublic.model_validate_json(response_post.text)
        assert response_post.status_code == 200
        assert db_pdf.original_filename == "test.pdf"
        assert db_pdf.uploaded_by == created_user.id

        # Try to upload the same file again
        response_post_again = client.post("/api/pdfs", files=files, headers=token_header)
        assert response_post_again.status_code == 200

        # Get uploaded test file from backend and compare contents with original
        response_get = client.get(f"api/pdfs/{db_pdf.id}.pdf", headers=token_header)
        pdf_file.seek(0)
        assert pdf_file.read() == response_get.content
        assert response_get.headers["content-type"] == "application/pdf"
        
        # Get the pdf object from database and validate
        response_get = client.get(f"api/pdfs/{db_pdf.id}", headers=token_header)
        assert response_get.status_code == 200
        PdfPublic.model_validate_json(response_get.text)
        
        # Update pdf object in database and validate
        new_data = PdfUpdate(original_filename="wasd.pdf")
        response_patch = client.patch(f"api/pdfs/{db_pdf.id}",
                headers=token_header, json=new_data.model_dump(exclude_unset=True))
        updated_pdf = PdfPublic.model_validate_json(response_patch.text)
        assert updated_pdf == PdfPublic.model_validate(
        db_pdf, update={"original_filename": "wasd.pdf"})
        
        # remove uploaded test file
        response_delete = client.delete(f"api/pdfs/{db_pdf.id}.pdf", headers=token_header)
        assert response_delete.status_code == 200
        # Make sure file was removed
        response_after_delete = client.get(f"api/pdfs/{db_pdf.id}.pdf", headers=token_header)
        assert response_after_delete.status_code == 404
        
        # remove pdf database entry
        response_delete = client.delete(f"api/pdfs/{db_pdf.id}", headers=token_header)
        assert response_delete.status_code == 200
        # Make sure entry was removed
        response_after_delete = client.get(f"api/pdfs/{db_pdf.id}", headers=token_header)
        assert response_after_delete.status_code == 404


def test_post_with_missing_data(session: Session, client: TestClient):
    user_crud.create_user(session, test_user)
    token_header = _get_access_token_header(client, test_email, test_password)

    response = client.post("/api/pdfs", files={'pdf_file': ""}, headers=token_header)
    assert response.status_code == 422

    response = client.post("/api/pdfs", headers=token_header)
    assert response.status_code == 422

    response = client.post("/api/pdfs", data={"test": "test"}, headers=token_header)
    assert response.status_code == 422


def test_post_with_infected_mockup(session: Session, client: TestClient, mocker):
    user_crud.create_user(session, test_user)
    token_header = _get_access_token_header(client, test_email, test_password)
    
    with open("backend/tests/api/test.pdf", "rb") as pdf_file:

        # Mock ClamAV scan result with infected file
        mocker.patch("backend.app.api.scanners.Scanners.scan", return_value={"clamav": Response(406)})

        # Upload test pdf file
        response_post = client.post("/api/pdfs", files={'pdf_file': pdf_file},
                                    headers=token_header)
        assert response_post.status_code == 406


def test_delete_invalid_id(session: Session, client: TestClient):
    user_crud.create_user(session, test_user)
    token_header = _get_access_token_header(client, test_email, test_password)

    invalid_id = "invalid"
    response_delete = client.delete(f"api/pdfs/{invalid_id}", headers=token_header)
    assert response_delete.status_code == 404

    response_delete = client.delete(f"api/pdfs/{invalid_id}.pdf", headers=token_header)
    assert response_delete.status_code == 404
