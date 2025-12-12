"""
create, read, update, and delete (CRUD) users for the database

Based on: 
https://github.com/fastapi/full-stack-fastapi-template/blob/e4022a9502a6b61c857e3cbdaddc69e7219c9d53/backend/app/crud.py
"""
# pylint: disable=import-error, missing-function-docstring, line-too-long, fixme

import uuid
from sqlmodel import Session, select

from app.security import get_password_hash, verify_password
from app.models import User, UserCreate, UserUpdate
from app.api.depdendancies import CurrentUser


def create_user(session: Session, user_create: UserCreate) -> User:
    db_user = User.model_validate(
        user_create, update={
            "hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def update_user(session: Session, current_user: CurrentUser, user_update: UserUpdate) -> User:
    new_data = user_update.model_dump(exclude_unset=True)

    current_user.sqlmodel_update(new_data)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user


def delete_user(session: Session,  user_id: uuid.UUID | str):
    if isinstance(user_id, str):
        user_id = uuid.UUID(user_id)

    target_user = get_user_by_id(session, user_id)
    session.delete(target_user)
    session.commit()


def get_user_by_id(session: Session, user_id: uuid.UUID | str):
    if isinstance(user_id, str):
        user_id = uuid.UUID(user_id)

    db_user = session.get(User, user_id)
    return db_user


def get_user_by_email(session: Session, email: str) -> User | None:
    user_with_email = select(User).where(User.email == email)
    session_user = session.exec(user_with_email).first()
    return session_user


def authenticate_user(session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session, email)
    if not db_user:
        # No user with given email
        return None
    if not verify_password(password, db_user.hashed_password):
        # Given password and stored password hash didn't match
        return None

    # User was found in database and password hash matched
    return db_user
