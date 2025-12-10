"""
Unit tests for /api/users and /api/login
"""
# pylint: disable=invalid-name, missing-function-docstring, import-error
import uuid
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import UserCreate
from app import crud


test_email = "foo@bar.com"
test_password = "foobarbaz"
test_login = {"username": test_email,
              "password": test_password}
test_user = UserCreate(email=test_email, password=test_password)


def _get_test_access_token(client: TestClient):
    response_token = client.post("/api/login/access-token", data=test_login)
    return response_token.json()


def _get_test_access_token_header(client: TestClient):
    token = _get_test_access_token(client)
    return {"Authorization": f"Bearer {token}"}


def test_get_users_me(client: TestClient, session: Session):
    crud.create_user(session, test_user)
    token_header = _get_test_access_token_header(client)

    # Get current user from api
    response_me = client.get("/api/users/me", headers=token_header)
    assert response_me.status_code == 200


def test_get_users_me_invalid_token(client: TestClient, session: Session):
    crud.create_user(session, test_user)
    token = "invalid"
    token_header = {"Authorization": f"Bearer {token}"}

    # Get current user from api
    response_me = client.get("/api/users/me", headers=token_header)
    assert response_me.status_code == 403


def test_get_users(client: TestClient, session: Session):
    created_user = crud.create_user(session, test_user)
    token_header = _get_test_access_token_header(client)

    # Get user with user id
    response = client.get(
        f"/api/users/{created_user.id}", headers=token_header)
    data = response.json()
    assert response.status_code == 200
    assert data["email"] == test_user.email


def test_get_users_invalid_token(client: TestClient, session: Session):
    created_user = crud.create_user(session, test_user)
    token = "invalid"
    token_header = {"Authorization": f"Bearer {token}"}

    # Get user with user id
    response = client.get(
        f"/api/users/{created_user.id}", headers=token_header)
    assert response.status_code == 403


def test_get_users_invalid_id(client: TestClient, session: Session):
    crud.create_user(session, test_user)
    token_header = _get_test_access_token_header(client)

    # Get user with user id that doesn't exist in the database
    invalid_id = uuid.UUID(int=0xDEADBEEF)
    response = client.get(f"/api/users/{invalid_id}", headers=token_header)
    assert response.status_code == 404


def test_signup(client: TestClient):
    response = client.post("/api/users/signup", json=test_user.model_dump())
    assert response.status_code == 200
    assert response.json()["email"] == test_email
