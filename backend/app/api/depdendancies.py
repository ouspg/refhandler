from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlmodel import Session
import jwt

from app.db import engine
from app.api.scanners import Scanners
from app.models import User
from app import security

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/login/access-token"
)

def get_session():
    with Session(engine) as session:
        yield session

# Used for injecting dependancies at API endpoint creation
SessionDep = Annotated[Session, Depends(get_session)]
ScannersDep = Annotated[Scanners, Depends(Scanners)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]
OAuth2Dep = Annotated[OAuth2PasswordRequestForm, Depends()]

def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        decoded_token = jwt.decode(token, security.SECRET_KEY, security.ALGORITHM)
    except (jwt.InvalidTokenError):
        raise HTTPException(403, "Could not decode token")
    
    user = session.get(User, decoded_token["subject"])
    
    if not user:
        raise HTTPException(404, "User not found")
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]