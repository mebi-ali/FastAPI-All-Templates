
# user_service/api/deps.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError

from user_service.db import DBSessionDep
from user_service.core import security
from user_service.auth.schemas import TokenPayload
from user_service.user import user_service, schemas as user_schemas
from user_service.common import custom_exceptions

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    db: DBSessionDep,
    token: str = Depends(oauth2_scheme),
    
) -> user_schemas.UserOut:
    try:
        payload = security.decode_access_token(token)
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise custom_exceptions.UnauthorizedException("Could not validate credentials")

    user = await user_service.get_by_email(db, email=token_data.sub)
    if not user:
        raise custom_exceptions.UnauthorizedException("User not found")

    return user
