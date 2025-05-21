# api/v1/auth.py

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from user_service.auth.schemas import LoginRequest, LoginResponse
from user_service.user.schemas import UserCreate, UserOut
from user_service.auth.service import auth_service
from user_service.api.deps import get_current_user
from user_service.db import DBSessionDep
from user_service.common import custom_exceptions

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=LoginResponse)
async def login(
    conn: DBSessionDep,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    return await auth_service.authenticate_user(
        conn,
        login_data=LoginRequest(email=form_data.username, password=form_data.password),
    )

@router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserCreate,
    conn: DBSessionDep,
):
    try:
        return await auth_service.signup_user(conn, user_data)
    except custom_exceptions.BadRequestException as e:
        raise e


@router.get("/me", response_model=UserOut)
async def get_me(current_user: UserOut = Depends(get_current_user)):
    return current_user


@router.post("/refresh", response_model=LoginResponse)
async def refresh_token(current_user: UserOut = Depends(get_current_user)):
    access_token = auth_service.create_token_for_user(current_user)
    expires_at = None  # Optional: calculate based on token TTL if needed
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_at=expires_at,
    )
