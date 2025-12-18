"""
Database operations for (CRUD) creating, reading, updating and deleting users

Based on: 
https://github.com/fastapi/full-stack-fastapi-template/blob/e4022a9502a6b61c857e3cbdaddc69e7219c9d53/backend/app/crud.py
"""
# pylint: disable=missing-function-docstring, line-too-long, fixme

import uuid
import os
from sqlmodel import Session, select

from backend.app.security import get_password_hash, verify_password
from backend.app.models import User, UserCreate, UserUpdate, UserRole

ADMIN_EMAIL = os.environ["ADMIN_EMAIL"]
ADMIN_PASSWORD = os.environ["ADMIN_PASSWORD"]


def create_user(session: Session, user_create: UserCreate) -> User | None:
    """Inserts user_create into the database, returns None if user email was already in use"""
    # Skip user creation if email is already in use
    if get_user_by_email(session, user_create.email):
        return None

    # Replace plaintext password with hash and insert User into database
    db_user = User.model_validate(
        user_create, update={
            "hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def create_default_admin(session: Session) -> User | None:
    """Inserts default admin User into the database, returns None if already exists"""
    admin_user = UserCreate(role=UserRole.admin, email=ADMIN_EMAIL, password=ADMIN_PASSWORD)
    return create_user(session, admin_user)


def update_user(session: Session, target_user: User, user_update: UserUpdate) -> User:
    """Updates target_user database entry with new values from user_update"""
    new_data = user_update.model_dump(exclude_unset=True)

    extra_data = {}
    if "password" in new_data and new_data["password"] is not None:
        password = new_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    
    target_user.sqlmodel_update(new_data, update=extra_data)
    session.add(target_user)
    session.commit()
    session.refresh(target_user)
    return target_user


def delete_user(session: Session,  target_user: User):
    """Deletes target_user from the database"""
    session.delete(target_user)
    session.commit()


def get_user_by_id(session: Session, user_id: uuid.UUID | str) -> User | None:
    """Returns User from database matching user_id, returns None if User wasn't found"""

    # Accept UUID in str format, but convert it to UUID
    try:
        if isinstance(user_id, str):
            user_id = uuid.UUID(user_id)
    except ValueError:
        # String wasn't a valid UUID
        return None

    # Returns None if User matching user_id wasn't found
    db_user = session.get(User, user_id)
    return db_user


def get_user_by_email(session: Session, email: str) -> User | None:
    """Returns User from database with email, returns None if User wasn't found"""
    user_with_email = select(User).where(User.email == email)
    session_user = session.exec(user_with_email).first()
    return session_user


def authenticate_user(session: Session, email: str, password: str) -> User | None:
    """Returns User from database matching credentials email:password,
    returns None if User wasnt found or password didn't match stored hash"""
    
    db_user = get_user_by_email(session, email)
    if not db_user:
        # No user with given email
        return None
    if not verify_password(password, db_user.hashed_password):
        # Given password and stored password hash didn't match
        return None

    # User was found in database and password hash matched
    return db_user
