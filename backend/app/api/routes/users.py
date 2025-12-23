"""
API definitions for /api/users

If the API function has types CurrentUser or CurrentAdmin as an argument,
using the API endpoint requires a valid access token header.
CurrentAdmin additionally requires the user to have the role UserRole.admin.

(see API documentation in /backend/README.md for details)
"""
# pylint: disable=missing-function-docstring, missing-module-docstring, unused-argument
from fastapi import APIRouter, HTTPException

from backend.app.api import user_crud
from backend.app.api.depdendancies import SessionDep, CurrentUser, CurrentAdmin
from backend.app.models import UserCreate, UserUpdate, UserRole, UserPublic

router = APIRouter()


# Get currently authenticated user
@router.get("/me", response_model=UserPublic)
async def get_user_me(current_user: CurrentUser):
    return current_user


# Update currently authenticated user
@router.patch("/me", response_model=UserPublic)
async def update_user_me(session: SessionDep, current_user: CurrentUser, user_update: UserUpdate):
    if user_update.email:
        existing_user = user_crud.get_user_by_email(session, user_update.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(409, f"User with email {user_update.email} already exits")

    updated_user = user_crud.update_user(session, current_user, user_update)
    return updated_user


# Delete currently authenticated user
@router.delete("/me")
async def delete_user_me(session: SessionDep, current_user: CurrentUser):
    if current_user.role == UserRole.admin:
        raise HTTPException(403, "Admin users shouldn't be deleted")

    user_crud.delete_user(session, current_user)
    return {"message": f"User {current_user.email} deleted sucessfully"}


# Get user with UUID user_id
@router.get("/{user_id}", response_model=UserPublic)
async def get_user(session: SessionDep, current_user: CurrentUser, user_id: str):
    user = user_crud.get_user_by_id(session, user_id)

    if not user:
        raise HTTPException(404, "User not found")

    return user


# Update user with UUID user_id (Admin only)
@router.patch("/{user_id}", response_model=UserPublic)
async def update_user(session: SessionDep, current_admin: CurrentAdmin,
                    user_update: UserUpdate, user_id: str):

    target_user = user_crud.get_user_by_id(session, user_id)
    if target_user is None:
        raise HTTPException(404, "User not found")
    
    if user_update.email:
        existing_user = user_crud.get_user_by_email(session, user_update.email)
        if existing_user and existing_user.id != target_user.id:
            raise HTTPException(409, f"User with email {user_update.email} already exits")

    updated_user = user_crud.update_user(session, target_user, user_update)
    return updated_user


# Delete user with UUID user_id (Admin only)
@router.delete("/{user_id}")
async def delete_user(session: SessionDep, current_admin: CurrentAdmin, user_id: str):

    target_user = user_crud.get_user_by_id(session, user_id)
    if target_user is None:
        raise HTTPException(404, "User not found")

    user_crud.delete_user(session, target_user)
    return {"message": f"User {target_user.email} deleted sucessfully"}


# Register new user account
@router.post("/signup", response_model=UserPublic)
async def register_user(session: SessionDep, new_user: UserCreate):

    existing_user = user_crud.get_user_by_email(session, new_user.email)

    if existing_user:
        raise HTTPException(400, "User with given email alrady exists")

    userCreate = UserCreate.model_validate(new_user)
    user = user_crud.create_user(session, userCreate)
    return user
