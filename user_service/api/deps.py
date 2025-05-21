from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from pydantic import ValidationError
from asyncpg import Connection

from user_service.db import DBSessionDep
from user_service.core import security
from user_service.auth.schemas import TokenPayload
from user_service.user.models import UserModel  # ✅ Import model directly
from user_service.common import custom_exceptions

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    conn: DBSessionDep,
    token: str = Depends(oauth2_scheme),
) -> UserModel:  
    try:
        payload = security.decode_access_token(token)
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise custom_exceptions.UnauthorizedException("Could not validate credentials")

    user = await UserModel.get(conn=conn, email=token_data.sub, is_deleted=False)
    if not user:
        raise custom_exceptions.UnauthorizedException("User not found")

    return user


async def get_current_active_superuser(
    current_user: UserModel = Depends(get_current_user)  # ✅ Full model allows access checks
) -> UserModel:
    if not current_user.is_superuser:
        raise custom_exceptions.UnauthorizedException("Insufficient privileges")
    return current_user

