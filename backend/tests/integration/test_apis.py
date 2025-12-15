"""
Integration tests for the API endpoints

docker_services in function argument means pytest-docker is used to run
the docker compose stack before running tests. (see conftest.py for details)
"""
# pylint: disable=missing-function-docstring, unused-argument, unused-import
import os
import pytest
import requests
from backend.app.models import UserCreate, UserUpdate, UserPublic, UserRole, PdfPublic


test_email = "foo@bar.com"
test_password = "foobarbaz"
test_user = UserCreate(email=test_email, password=test_password)

ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", 'NO ADMIN_EMAIL IN ENVIRONMENT')
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", 'NO ADMIN_PASSWORD IN ENVIRONMENT')


def _get_oauth2_login(username: str, password: str):
    return {"username": username, "password": password }

def _get_access_token_header(api_url, username: str, password: str):
    login = _get_oauth2_login(username, password)
    url = api_url + "/login/access-token"
    response_token = requests.post(url, data=login, timeout=10)
    token = response_token.json()
    return {"Authorization": f"Bearer {token}"}


def test_get_default_admin_token(api_url, docker_services):
    token_header = _get_access_token_header(api_url, ADMIN_EMAIL, ADMIN_PASSWORD)
    assert token_header is not None


def test_api_users(api_url, docker_services):
    # Signup test_user
    response = requests.post(f"{api_url}/users/signup", json=test_user.model_dump(), timeout=20)
    assert response.status_code == 200
    assert response.json()["email"] == test_email

    # Get token header for test_user
    header = _get_access_token_header(api_url, test_email, test_password)
    assert header is not None

    # Get current user from api
    response = requests.get(f"{api_url}/users/me", headers=header, timeout=20)
    assert response.status_code == 200
    assert response.json()["email"] == test_email

    # Change current user email,role and password
    new_email = "foofoo@barbar.com"
    new_data = UserUpdate(email=new_email, role=UserRole.manager, password="new_password")

    response = requests.patch(f"{api_url}/users/me",
                            headers=header, json=new_data.model_dump(), timeout=20)
    assert response.status_code == 200
    updated_user = UserPublic.model_validate_json(response.text)
    assert updated_user.email == new_email
    assert updated_user.role == UserRole.manager

    # Get test_user using user_id
    response = requests.get(f"{api_url}/users/{updated_user.id}", headers=header, timeout=20)
    assert response.status_code == 200
    get_user = UserPublic.model_validate_json(response.text)
    assert get_user.email == new_email

    # Delete test_user
    response = requests.delete(f"{api_url}/users/me", headers=header, timeout=20)
    assert response.status_code == 200

    # Make sure test_user was deleted
    response = requests.delete(f"{api_url}/users/me", headers=header, timeout=20)
    assert response.status_code == 404
    response = requests.delete(f"{api_url}/users/{updated_user.id}", headers=header, timeout=20)
    assert response.status_code == 404


def test_api_pdfs(api_url, docker_services):
    header = _get_access_token_header(api_url, ADMIN_EMAIL, ADMIN_PASSWORD)
    with open("backend/tests/api/test.pdf", "rb") as pdf_file:
        # Upload test pdf file
        files = {"pdf_file": pdf_file}
        response_post = requests.post(f"{api_url}/pdfs", files=files, headers=header, timeout=20)

        db_pdf = PdfPublic.model_validate_json(response_post.text)
        assert response_post.status_code == 200
        assert db_pdf.original_filename == "test.pdf"

        # Try to upload the same file again
        pdf_file.seek(0)
        response_post_again = requests.post(f"{api_url}/pdfs", files=files, headers=header, timeout=20)
        assert response_post_again.status_code == 409

        # Get uploaded test file from backend and compare contents with original
        response_get = requests.get(f"{api_url}/pdfs/{db_pdf.id}.pdf", headers=header, timeout=20)
        pdf_file.seek(0)
        assert pdf_file.read() == response_get.content
        assert response_get.headers["content-type"] == "application/pdf"

        # Get the pdf object from database
        response_get = requests.get(f"{api_url}/pdfs/{db_pdf.id}", headers=header, timeout=20)
        assert response_get.status_code == 200

        # remove uploaded test file
        response_delete = requests.delete(f"{api_url}/pdfs/{db_pdf.id}", headers=header, timeout=20)
        assert response_delete.status_code == 200

        # Make sure file was removed
        response_after_delete = requests.get(f"{api_url}/pdfs/{db_pdf.id}.pdf", headers=header, timeout=20)
        assert response_after_delete.status_code == 404
        response_after_delete = requests.get(f"{api_url}/pdfs/{db_pdf.id}", headers=header, timeout=20)
        assert response_after_delete.status_code == 404
