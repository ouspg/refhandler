# Based on: https://github.com/fastapi/full-stack-fastapi-template/blob/e4022a9502a6b61c857e3cbdaddc69e7219c9d53/backend/app/crud.py

import uuid
from sqlmodel import Session, select

from app.security import get_password_hash, verify_password
from app.models import User, UserCreate

def create_user(session: Session, userCreate: UserCreate) -> User:
    db_user = User.model_validate(
        userCreate, update={"hashed_password": get_password_hash(userCreate.password)}
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

#TODO: update_user

def get_user_by_email(session: Session, email: str) -> User | None:
    user_with_email = select(User).where(User.email == email)
    session_user = session.exec(user_with_email).first()
    return session_user

def authenticate(session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session, email)
    if not db_user:
        # No user with given email
        return None
    if not verify_password(password, db_user.hashed_password):
        # Given password and stored password hash didn't match
        return None
    
    # User was found in database and password hash matched
    return db_user