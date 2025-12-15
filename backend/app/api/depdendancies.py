# pylint: disable=missing-function-docstring, line-too-long
"""
Dependancies that can be injected into the FastAPI endpoint functions.

SessionDep: Contains database session that API endpoints will use for database operations
ScannersDep: Contains malware scanners, used by /api/pdfs

OAuth2Dep: For /api/login credentials form
TokenDep: For JWT token decoding in get_current_user() 
CurrentUser: For authenticating API endpoints. Checks if the API call has a valid JWT token.
CurrentAdmin: Same as CurrentUser, but requires the authenticated user to have the role UserRole.admin
"""

from typing import Annotated
import uuid
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlmodel import Session
import jwt

from backend.app.postgres_db import engine
from backend.app.api.scanners import Scanners
from backend.app.models import User, UserRole
from backend.app import security

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/login/access-token"
)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
ScannersDep = Annotated[Scanners, Depends(Scanners)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]
OAuth2Dep = Annotated[OAuth2PasswordRequestForm, Depends()]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        decoded_token = jwt.decode(
            token, security.SECRET_KEY, security.ALGORITHM)
    except jwt.InvalidTokenError as e:
        raise HTTPException(403, "Could not decode token") from e

    user_id = uuid.UUID(decoded_token["subject"])
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(404, "User not found")
    return user


def get_current_admin(session: SessionDep, token: TokenDep) -> User:
    user = get_current_user(session, token)

    if user.role != UserRole.admin:
        raise HTTPException(403, "Use role isn't admin")

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentAdmin = Annotated[User, Depends(get_current_admin)]
