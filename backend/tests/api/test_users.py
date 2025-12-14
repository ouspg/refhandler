"""
Unit tests for /api/users and /api/login
"""
# pylint: disable=missing-function-docstring
import uuid
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.app.models import UserCreate, UserUpdate, UserRole
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


def test_get_users_me(client: TestClient, session: Session):
    user_crud.create_user(session, test_user)
    token_header = _get_access_token_header(client, test_email, test_password)

    # Get current user from api
    response = client.get("/api/users/me", headers=token_header)
    assert response.status_code == 200


def test_get_users_me_invalid_token(client: TestClient, session: Session):
    user_crud.create_user(session, test_user)
    token = "invalid"
    token_header = {"Authorization": f"Bearer {token}"}

    # Get current user from api
    response = client.get("/api/users/me", headers=token_header)
    assert response.status_code == 403


def test_update_users_me(client: TestClient, session: Session):
    created_user = user_crud.create_user(session, test_user)
    token_header = _get_access_token_header(client, test_email, test_password)
    new_email = "foofoo@barbar.com"
    new_data = UserUpdate(email=new_email)

    response = client.patch(
        "/api/users/me", headers=token_header, json=new_data.model_dump())
    assert response.status_code == 200
    assert created_user.email == new_email


def test_update_users_me_email_in_use(client: TestClient, session: Session):
    user1 = user_crud.create_user(session, UserCreate(email=test_email, password=test_password))
    user2 = user_crud.create_user(session, UserCreate(
        email="foofoo@barbar.com", password=test_password))
    user1_token_header = _get_access_token_header(client, test_email, test_password)

    # Try to update first user's email to second user's email
    new_data = UserUpdate(email=user2.email)
    response = client.patch(
        "/api/users/me", headers=user1_token_header, json=new_data.model_dump())
    assert response.status_code == 409
    assert user1.email != user2.email


def test_delete_users_me(client: TestClient, session: Session):
    user_crud.create_user(session, test_user)
    token_header = _get_access_token_header(client, test_email, test_password)

    # Delete current user
    response = client.delete("/api/users/me", headers=token_header)
    assert response.status_code == 200
    
    # Get a new token for the deleted user, should fail with code 400
    login = _get_oauth2_login(test_email, test_password)
    response_token = client.post("/api/login/access-token", data=login)
    assert response_token.status_code == 400


def test_get_users(client: TestClient, session: Session):
    created_user = user_crud.create_user(session, test_user)
    token_header = _get_access_token_header(client, test_email, test_password)

    # Get user with user id
    response = client.get(
        f"/api/users/{created_user.id}", headers=token_header)
    data = response.json()
    assert response.status_code == 200
    assert data["email"] == test_user.email


def test_get_users_invalid_token(client: TestClient, session: Session):
    created_user = user_crud.create_user(session, test_user)
    token = "invalid"
    token_header = {"Authorization": f"Bearer {token}"}

    # Get user with user id
    response = client.get(
        f"/api/users/{created_user.id}", headers=token_header)
    assert response.status_code == 403


def test_get_users_invalid_id(client: TestClient, session: Session):
    user_crud.create_user(session, test_user)
    token_header = _get_access_token_header(client, test_email, test_password)

    # Get user with user id that doesn't exist in the database
    invalid_id = uuid.UUID(int=0xDEADBEEF)
    response = client.get(f"/api/users/{invalid_id}", headers=token_header)
    assert response.status_code == 404


def test_update_user_by_admin(client: TestClient, session: Session):
    created_user = user_crud.create_user(session, test_user)
    user_crud.create_user(session, test_admin)
    admin_token_header = _get_access_token_header(
        client, test_admin.email, test_admin.password)
    new_email = "new@email.com"
    new_data = UserUpdate(email=new_email)

    # Update other user's email using the admin user
    api_string = f"/api/users/{created_user.id}"
    response = client.patch(
        api_string, headers=admin_token_header, json=new_data.model_dump())

    updated_email = response.json()["email"]
    assert response.status_code == 200
    assert updated_email == new_email


def test_update_user_by_other_user(client: TestClient, session: Session):
    user1 = user_crud.create_user(session, UserCreate(email=test_email, password=test_password))
    user2 = user_crud.create_user(session, UserCreate(
        email="foofoo@barbar.com", password=test_password))
    user1_token_header = _get_access_token_header(client, test_email, test_password)

    # Try to update second user's email using first user
    new_data = UserUpdate(email="new@email.com")
    api_string = f"/api/users/{user2.id}"
    response = client.patch(
        api_string, headers=user1_token_header, json=new_data.model_dump())
    assert response.status_code == 403
    assert user2.email != "new@email.com"


def test_delete_user_by_admin(client: TestClient, session: Session):
    created_user = user_crud.create_user(session, test_user)
    user_crud.create_user(session, test_admin)
    admin_token_header = _get_access_token_header(
        client, test_admin.email, test_admin.password)

    # Delete other user using the admin account
    api_string = f"/api/users/{created_user.id}"
    response = client.delete(api_string, headers=admin_token_header)
    assert response.status_code == 200
    assert user_crud.get_user_by_id(session, created_user.id) is None


def test_delete_user_by_other_user(client: TestClient, session: Session):
    user1 = user_crud.create_user(session, UserCreate(email=test_email, password=test_password))
    user2 = user_crud.create_user(session, UserCreate(
        email="foofoo@barbar.com", password=test_password))
    user1_token_header = _get_access_token_header(client, test_email, test_password)

    # Try to delete second user using first user
    api_string = f"/api/users/{user2.id}"
    response = client.delete(api_string, headers=user1_token_header)
    assert response.status_code == 403
    assert user_crud.get_user_by_id(session, user2.id) is not None


def test_signup(client: TestClient):
    response = client.post("/api/users/signup", json=test_user.model_dump())
    assert response.status_code == 200
    assert response.json()["email"] == test_email
