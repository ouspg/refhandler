from fastapi import APIRouter, HTTPException

from app import crud, security
from app.api.depdendancies import SessionDep, OAuth2Dep

router = APIRouter()

@router.post("/access-token")
def create_login_access_token(session: SessionDep, form_data: OAuth2Dep):
    user = crud.authenticate_user(session, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(400, "Incorrect email or password")
    
    return security.create_jwt_token(user.id)