#user_service/api/v1/user.py

from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from typing import List

from pydantic import EmailStr
from user_service.db import DBSessionDep
from user_service.user import schemas
from user_service.user.service import user_service
from user_service.api.deps import get_current_user, get_current_active_superuser
from user_service.common import custom_exceptions

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[schemas.UserOut])
async def list_users(
    conn: DBSessionDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    filters: schemas.UserFilters = Depends(),
    current_user: schemas.UserOut = Depends(get_current_active_superuser),
):
    return await user_service.get_all_users(conn=conn, skip=skip, limit=limit, filters=filters)


@router.get("/me", response_model=schemas.UserOut)
async def get_me(current_user: schemas.UserOut = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=schemas.UserOut)
async def get_user_by_id(
    user_id: UUID,
    conn: DBSessionDep,
    current_user: schemas.UserOut = Depends(get_current_active_superuser),
):
    return await user_service.get_user_by_id(conn, user_id)



@router.get("/email/{email}", response_model=schemas.UserOut)
async def get_user_by_email(
    email: EmailStr,
    conn: DBSessionDep,
    current_user: schemas.UserOut = Depends(get_current_active_superuser),
):
    return await user_service.get_by_email(conn, email)



@router.put("/{user_id}", response_model=schemas.UserOut)
async def update_user(
    user_id: UUID,
    user_in: schemas.UserUpdate,
    conn: DBSessionDep,
    current_user: schemas.UserOut = Depends(get_current_user),
):
    if current_user.id != user_id and not current_user.is_superuser:
        raise custom_exceptions.UnauthorizedException("You are not allowed to update this user", {"user_id": user_id})
    return await user_service.update_user(conn, user_id, user_in)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    conn: DBSessionDep,
    current_user: schemas.UserOut = Depends(get_current_active_superuser),
):
    await user_service.delete_user(conn, user_id)
    return {"detail": "User deleted"}


@router.post("/{user_id}/password", response_model=schemas.UserOut)
async def update_user_password(
    conn: DBSessionDep,
    user_id: UUID,
    new_password: str,
    old_password: str = "",
    verify_old: bool = False,
    
    current_user: schemas.UserOut = Depends(get_current_user),
):
    if current_user.id != user_id and not current_user.is_superuser:
        raise custom_exceptions.UnauthorizedException("You are not allowed to update this user's password", {"user_id": user_id})

    return await user_service.update_password(
        conn=conn,
        user_id=user_id,
        new_password=new_password,
        old_password=old_password,
        verify_old=verify_old,
    )
