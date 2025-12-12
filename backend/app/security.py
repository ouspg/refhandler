# pylint: disable=import-error, missing-function-docstring, missing-module-docstring, line-too-long
# Based on: https://github.com/fastapi/full-stack-fastapi-template/blob/master/backend/app/core/security.py

from datetime import datetime, timedelta, timezone
from typing import Any
import os
import jwt
from passlib.context import CryptContext

ALGORITHM = "HS256"
SECRET_KEY = str(os.environ.get("SECRET_KEY", 'NO SECRET_KEY IN ENVIRONMENT'))
EXPIRATION = timedelta(weeks=1)

cc = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_jwt_token(subject: str | Any, expires_delta: timedelta = EXPIRATION) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    encoded_jwt = jwt.encode(payload={"expiration": expire.isoformat(), "subject": str(subject)},
                             key=SECRET_KEY,
                             algorithm=ALGORITHM
                             )
    return encoded_jwt


def verify_password(password: str, hashed_password: str) -> bool:
    return cc.verify(password, hashed_password)


def get_password_hash(password: str) -> str:
    return cc.hash(password)
