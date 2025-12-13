"""
Unit tests for backend.app.crud
"""
# pylint: disable=invalid-name, missing-function-docstring, import-error
import uuid
from sqlmodel import Session
from backend.app.models import UserCreate, UserUpdate
from backend.app import security
from backend.app.api import user_crud

test_email = "foo@bar.com"
test_password = "foobarbaz"
test_user = UserCreate(email=test_email, password=test_password)


def test_create_user(session: Session):
    created_user = user_crud.create_user(session, test_user)
    assert created_user.email == test_email
    assert isinstance(created_user.id, uuid.UUID)

    assert security.verify_password(
        test_password, created_user.hashed_password)


def test_update_user(session: Session):
    created_user = user_crud.create_user(session, test_user)
    new_email = "foofoo@barbar.com"
    new_data = UserUpdate(email=new_email)

    user_crud.update_user(session, created_user, new_data)
    assert created_user.email == new_email


def test_delete_user(session: Session):
    created_user = user_crud.create_user(session, test_user)

    user_crud.delete_user(session, created_user)
    assert user_crud.get_user_by_id(session, created_user.id) is None


def test_get_user_by_id(session: Session):
    created_user = user_crud.create_user(session, test_user)
    user_by_id = user_crud.get_user_by_id(session, created_user.id)

    assert user_by_id == created_user


def test_get_user_by_email(session: Session):
    created_user = user_crud.create_user(session, test_user)
    user_by_email = user_crud.get_user_by_email(session, test_email)

    assert user_by_email == created_user


def test_authenticate_user(session: Session):
    created_user = user_crud.create_user(session, test_user)
    authenticated_user = user_crud.authenticate_user(
        session, test_email, test_password)

    assert authenticated_user is created_user


def test_authenticate_user_invalid_email(session: Session):
    user_crud.create_user(session, test_user)
    invalid_email = "invalid@bar.com"
    authenticated_user = user_crud.authenticate_user(
        session, invalid_email, test_password)

    assert authenticated_user is None


def test_authenticate_user_invalid_password(session: Session):
    user_crud.create_user(session, test_user)
    invalid_password = "invalid"
    authenticated_user = user_crud.authenticate_user(
        session, test_email, invalid_password)

    assert authenticated_user is None
