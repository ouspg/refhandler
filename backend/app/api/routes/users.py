# pylint: disable=import-error, missing-function-docstring, missing-module-docstring, unused-argument
from fastapi import APIRouter, HTTPException

from app import crud
from app.api.depdendancies import SessionDep, CurrentUser
from app.models import UserCreate, UserUpdate, UserRole

router = APIRouter()


@router.get("/me")
async def get_user_me(current_user: CurrentUser):
    return current_user


@router.patch("/me")
async def update_user_me(session: SessionDep, current_user: CurrentUser, user_update: UserUpdate):
    if user_update.email:
        existing_user = crud.get_user_by_email(session, user_update.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(409, f"User with email {user_update.email} already exits")

    updated_user = crud.update_user(session, current_user, user_update)
    return updated_user


@router.delete("/me")
async def delete_user_me(session: SessionDep, current_user: CurrentUser):
    if current_user.role == UserRole.admin:
        raise HTTPException(403, "Admin users shouldn't be deleted")

    crud.delete_user(session, current_user.id)
    return {"message": f"User {current_user.email} deleted sucessfully"}


@router.get("/{user_id}")
async def get_user(session: SessionDep, current_user: CurrentUser, user_id: str):
    user = crud.get_user_by_id(session, user_id)

    if not user:
        raise HTTPException(404, "User not found")

    return user


@router.post("/signup")
async def register_user(session: SessionDep, new_user: UserCreate):

    existing_user = crud.get_user_by_email(session, new_user.email)

    if existing_user:
        raise HTTPException(400, "User with given email alrady exists")

    userCreate = UserCreate.model_validate(new_user)
    user = crud.create_user(session, userCreate)
    return user
