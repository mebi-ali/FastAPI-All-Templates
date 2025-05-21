# api/v1/auth.py

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from user_service.auth import schemas as auth_schemas
from user_service.auth.service import auth_service
from user_service.db import DBSessionDep, db_manager
from user_service.user import schemas as user_schemas
from user_service.api.deps import get_current_user

from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=auth_schemas.LoginResponse)
async def login(
    db: DBSessionDep,
    form_data: OAuth2PasswordRequestForm = Depends()
):
    login_data = auth_schemas.LoginRequest(email=form_data.username, password=form_data.password)
    response = await auth_service.authenticate_user(session=db, login_data=login_data)
    return response


@router.post("/signup", response_model=user_schemas.UserOut, status_code=status.HTTP_201_CREATED)
async def signup(user_data: user_schemas.UserCreate, db: DBSessionDep):
    new_user = await auth_service.signup_user(db, user_data)
    return new_user

@router.get("/me", response_model=user_schemas.UserOut)
async def get_current_user_profile(current_user: user_schemas.UserOut = Depends(get_current_user)):
    return current_user


@router.post("/refresh", response_model=auth_schemas.Token)
async def refresh_token(current_user: user_schemas.UserOut = Depends(get_current_user)):
    new_token = auth_service.create_token_for_user(current_user)
    return auth_schemas.Token(access_token=new_token, token_type="bearer")