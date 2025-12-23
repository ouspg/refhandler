"""
Unit tests for /api/login/access-token
"""
# pylint: disable=invalid-name, missing-function-docstring
from fastapi.testclient import TestClient
from sqlmodel import Session
from backend.app.api import user_crud
from backend.app.models import UserCreate



test_email = "foo@bar.com"
test_password = "foobarbaz"
test_login = {"username": test_email,
              "password": test_password}
test_user = UserCreate(email=test_email, password=test_password)


def test_get_access_token(client: TestClient, session: Session):
    user_crud.create_user(session, test_user)

    response = client.post("/api/login/access-token", data=test_login)
    assert response.status_code == 200


def test_get_access_token_invalid_user(client: TestClient, session: Session):
    user_crud.create_user(session, test_user)
    test_login["username"] = "invalid@bar.com"

    response = client.post("/api/login/access-token", data=test_login)
    assert response.status_code == 400


def test_get_access_token_invalid_password(client: TestClient, session: Session):
    user_crud.create_user(session, test_user)
    test_login["password"] = "invalid"

    response = client.post("/api/login/access-token", data=test_login)
    assert response.status_code == 400
