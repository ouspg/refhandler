"""
API definitions for /api/users

If the API function has 'current_user: CurrentUser' as an argument,
using the API endpoint requires a valid access token header
(see API documentation in /backend/README.md for details)
"""
# pylint: disable=import-error, missing-function-docstring, missing-module-docstring, unused-argument
from fastapi import APIRouter, HTTPException

from app import crud
from app.api.depdendancies import SessionDep, CurrentUser
from app.models import UserCreate, UserUpdate, UserRole

router = APIRouter()


# Get currently authenticated user
@router.get("/me")
async def get_user_me(current_user: CurrentUser):
    return current_user


# Update currently authenticated user
@router.patch("/me")
async def update_user_me(session: SessionDep, current_user: CurrentUser, user_update: UserUpdate):
    if user_update.email:
        existing_user = crud.get_user_by_email(session, user_update.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(409, f"User with email {user_update.email} already exits")

    updated_user = crud.update_user(session, current_user, user_update)
    return updated_user


# Delete currently authenticated user
@router.delete("/me")
async def delete_user_me(session: SessionDep, current_user: CurrentUser):
    if current_user.role == UserRole.admin:
        raise HTTPException(403, "Admin users shouldn't be deleted")

    crud.delete_user(session, current_user.id)
    return {"message": f"User {current_user.email} deleted sucessfully"}


# Get user with UUID user_id
@router.get("/{user_id}")
async def get_user(session: SessionDep, current_user: CurrentUser, user_id: str):
    user = crud.get_user_by_id(session, user_id)

    if not user:
        raise HTTPException(404, "User not found")

    return user


# Update user with UUID user_id (Admin only)
@router.patch("/{user_id}")
async def update_user(session: SessionDep, current_user: CurrentUser,
                    user_update: UserUpdate, user_id: str):
    if current_user.role != UserRole.admin:
        raise HTTPException(403, "Only Admin users can patch other users")

    if user_update.email:
        existing_user = crud.get_user_by_email(session, user_update.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(409, f"User with email {user_update.email} already exits")

    updated_user = crud.update_user(session, current_user, user_update)
    return updated_user


# Delete user with UUID user_id (Admin only)
@router.delete("/{user_id}")
async def delete_user(session: SessionDep, current_user: CurrentUser, user_id: str):
    if current_user.role != UserRole.admin:
        raise HTTPException(403, "Only Admin users can delete other users")

    crud.delete_user(session, user_id)
    return {"message": f"User {current_user.email} deleted sucessfully"}


# Register new user account
@router.post("/signup")
async def register_user(session: SessionDep, new_user: UserCreate):

    existing_user = crud.get_user_by_email(session, new_user.email)

    if existing_user:
        raise HTTPException(400, "User with given email alrady exists")

    userCreate = UserCreate.model_validate(new_user)
    user = crud.create_user(session, userCreate)
    return user
