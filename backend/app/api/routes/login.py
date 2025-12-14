# pylint: disable=missing-function-docstring, missing-module-docstring
from fastapi import APIRouter, HTTPException

from backend.app import security
from backend.app.api.depdendancies import SessionDep, OAuth2Dep
from backend.app.api import user_crud

router = APIRouter()


@router.post("/access-token")
def create_login_access_token(session: SessionDep, form_data: OAuth2Dep):
    user = user_crud.authenticate_user(
        session, form_data.username, form_data.password)

    if not user:
        raise HTTPException(400, "Incorrect email or password")

    return security.create_jwt_token(user.id)
