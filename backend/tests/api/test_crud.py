import pytest
import uuid
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.models import User, UserCreate
from app.crud import create_user, get_user_by_email, authenticate

def test_crud(client: TestClient, session: Session):
    test_email = "foo@bar.com"
    test_password = "foobar"
    test_user = UserCreate(email=test_email, password=test_password)
    
    created_user = create_user(session, test_user)
    assert created_user.email == test_email
    assert created_user.hashed_password != None
    assert type(created_user.id) == uuid.UUID

    user_by_email = get_user_by_email(session, test_email)
    assert user_by_email == created_user
    
    authenticated_user = authenticate(session, test_email, test_password)
    assert authenticated_user == created_user