#user_service/api/v1/user.py

from uuid import UUID
from pydantic import EmailStr
from fastapi import APIRouter, Depends, HTTPException, status
from user_service.user import schemas, models # UserCreate, UserRead, UserUpdate
from user_service.user import user_service
from user_service.db import DBSessionDep
from user_service.common import Pagination
from user_service.api.deps import get_current_user

from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: schemas.UserCreate, 
    db: DBSessionDep,
    current_user: models.UserModel = Depends(get_current_user)
):
    return await user_service.create_user(db, user_in)

@router.get("/{email}", response_model=schemas.UserOut)
async def get_user_by_email(email: EmailStr, db: DBSessionDep, current_user: models.UserModel = Depends(get_current_user)):
    return await user_service.get_by_email(db, email)


@router.get("/{user_id}", response_model=schemas.UserOut)
async def get_user_by_id(user_id: UUID, db: DBSessionDep, current_user: models.UserModel = Depends(get_current_user)):
    return await user_service.get_user_by_id(db, user_id)

# @router.get("/", response_model=list[schemas.UserOut])
# async def get_all_users(db: DBSessionDep, skip: int = 0, limit: int = 100, ):
#     return await user_service.get_all_users(db, skip, limit)

@router.get("/", response_model=list[schemas.UserOut])
async def get_all_users(
    db: DBSessionDep,
    filters: schemas.UserFilters = Depends(),
    pagination: Pagination = Depends(),
    current_user: models.UserModel = Depends(get_current_user)
):
    return await user_service.get_all_users(
        db,
        skip=pagination.skip,
        limit=pagination.limit,
        filters=filters,
    )

@router.put("/{user_id}", response_model=schemas.UserOut)
async def update_user(user_id: UUID, user_in: schemas.UserUpdate, db: DBSessionDep, current_user: models.UserModel = Depends(get_current_user)):
    return await user_service.update_user(db, user_id, user_in)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, db: DBSessionDep, current_user: models.UserModel = Depends(get_current_user)):
    await user_service.delete_user(db, user_id)
    return None
