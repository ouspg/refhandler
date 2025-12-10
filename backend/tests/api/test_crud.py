import pytest
import uuid
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.models import User, UserCreate
from app import crud, security

test_email = "foo@bar.com"
test_password = "foobarbaz"
test_user = UserCreate(email=test_email, password=test_password)

def test_create_user(client: TestClient, session: Session):
    created_user = crud.create_user(session, test_user)
    assert created_user.email == test_email
    assert type(created_user.id) == uuid.UUID
    
    hash = created_user.hashed_password
    assert security.verify_password(test_password, hash)

def test_get_user_by_id(client: TestClient, session: Session):
    created_user = crud.create_user(session, test_user)
    user_by_id = crud.get_user_by_id(session, created_user.id)

    assert user_by_id == created_user

def test_get_user_by_email(client: TestClient, session: Session):
    created_user = crud.create_user(session, test_user)
    user_by_email = crud.get_user_by_email(session, test_email)
    
    assert user_by_email == created_user
    
def test_authenticate_user(client: TestClient, session: Session):
    created_user = crud.create_user(session, test_user)
    authenticated_user = crud.authenticate_user(session, test_email, test_password)
    
    assert authenticated_user == created_user
    
def test_authenticate_user_invalid_email(client: TestClient, session: Session):
    created_user = crud.create_user(session, test_user)
    invalid_email = "invalid@bar.com"
    authenticated_user = crud.authenticate_user(session, invalid_email, test_password)
    
    assert authenticated_user == None
    
def test_authenticate_user_invalid_password(client: TestClient, session: Session):
    created_user = crud.create_user(session, test_user)
    invalid_password = "invalid"
    authenticated_user = crud.authenticate_user(session, test_email, invalid_password)
    
    assert authenticated_user == None