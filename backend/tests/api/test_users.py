"""
Unit tests for /api/users and /api/login
"""
# pylint: disable=invalid-name, missing-function-docstring, import-error
import uuid
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import UserCreate, UserUpdate
from app import crud


test_email = "foo@bar.com"
test_password = "foobarbaz"
test_login = {"username": test_email,
              "password": test_password}
test_user = UserCreate(email=test_email, password=test_password)


def _get_access_token(client: TestClient,  login: dict[str, str]):
    response_token = client.post("/api/login/access-token", data=login)
    return response_token.json()


def _get_access_token_header(client: TestClient, login: dict[str, str]):
    token = _get_access_token(client, login)
    return {"Authorization": f"Bearer {token}"}


def test_get_users_me(client: TestClient, session: Session):
    crud.create_user(session, test_user)
    token_header = _get_access_token_header(client, test_login)

    # Get current user from api
    response = client.get("/api/users/me", headers=token_header)
    assert response.status_code == 200


def test_get_users_me_invalid_token(client: TestClient, session: Session):
    crud.create_user(session, test_user)
    token = "invalid"
    token_header = {"Authorization": f"Bearer {token}"}

    # Get current user from api
    response = client.get("/api/users/me", headers=token_header)
    assert response.status_code == 403


def test_update_users_me(client: TestClient, session: Session):
    created_user = crud.create_user(session, test_user)
    token_header = _get_access_token_header(client, test_login)
    new_email = "foofoo@barbar.com"
    new_data = UserUpdate(email=new_email)

    response = client.patch(
        "/api/users/me", headers=token_header, json=new_data.model_dump())
    assert response.status_code == 200
    assert created_user.email == new_email


def test_update_users_me_email_in_use(client: TestClient, session: Session):
    user1 = crud.create_user(session, UserCreate(email=test_email, password=test_password))
    user2 = crud.create_user(session, UserCreate(
        email="foofoo@barbar.com", password=test_password))
    token_header = _get_access_token_header(client, test_login)

    # Try to update first user's email to second user's email
    new_data = UserUpdate(email=user2.email)
    response = client.patch(
        "/api/users/me", headers=token_header, json=new_data.model_dump())
    assert response.status_code == 409
    assert user1.email != user2.email


def test_delete_users_me(client: TestClient, session: Session):
    crud.create_user(session, test_user)
    token_header = _get_access_token_header(client, test_login)

    # Delete current user
    response = client.delete("/api/users/me", headers=token_header)
    assert response.status_code == 200
    
    # Get a new token for the deleted user, should fail with code 400
    response_token = client.post("/api/login/access-token", data=test_login)
    assert response_token.status_code == 400


def test_get_users(client: TestClient, session: Session):
    created_user = crud.create_user(session, test_user)
    token_header = _get_access_token_header(client, test_login)

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
    token_header = _get_access_token_header(client, test_login)

    # Get user with user id that doesn't exist in the database
    invalid_id = uuid.UUID(int=0xDEADBEEF)
    response = client.get(f"/api/users/{invalid_id}", headers=token_header)
    assert response.status_code == 404


def test_signup(client: TestClient):
    response = client.post("/api/users/signup", json=test_user.model_dump())
    assert response.status_code == 200
    assert response.json()["email"] == test_email
