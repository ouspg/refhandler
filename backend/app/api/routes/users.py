from fastapi import APIRouter, HTTPException

from app import crud, security
from app.api.depdendancies import SessionDep, OAuth2Dep, CurrentUser
from app.models import User

router = APIRouter()

@router.get("/me")
def get_user_me(current_user: CurrentUser):
    return current_user

@router.get("/{user_id}")
async def get_user(session: SessionDep, current_user: CurrentUser, user_id: str):
    user = crud.get_user_by_id(session, user_id)

    if not user:
        raise HTTPException(404, "User not found")
    
    return user