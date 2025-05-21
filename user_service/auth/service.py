# user_service/auth/service.py

from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from user_service.auth.schemas import LoginRequest, LoginResponse
from user_service.user.models import UserModel
from user_service.core import security
from user_service.user import user_service, schemas
from user_service.common import custom_exceptions, logger


class AuthService:
    async def authenticate_user(self, session: AsyncSession, login_data: LoginRequest) -> LoginResponse:
        # 1. Lookup user by email
        user: UserModel = await user_service.get_by_email(session, login_data.email)
        if not user:
            logger.warning(f"[AUTH] Failed login: Email not found - {login_data.email}")
            raise custom_exceptions.UnauthorizedException("Invalid credentials")

        if not security.verify_password(login_data.password, user.password):
            logger.warning(f"[AUTH] Failed login: Invalid password for {login_data.email}")
            raise custom_exceptions.UnauthorizedException("Invalid credentials")

        # Optional: Enforce email verification
        if not user.is_verified:
            logger.info(f"[AUTH] Unverified user tried to login - {user.email}")
            raise custom_exceptions.UnauthorizedException("Please verify your email to proceed")

        # Optional: Enforce account status
        if user.is_deleted or not user.is_active:
            logger.info(f"[AUTH] Inactive or deleted user attempted login - {user.email}")
            raise custom_exceptions.UnauthorizedException("Account is inactive or deleted")

        # Create access token
        token_data = {"sub": user.email}
        access_token = security.create_access_token(token_data)
        expires_at = datetime.utcnow() + timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)

        logger.info(f"[AUTH] User logged in successfully - {user.email}")

        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            expires_at=expires_at
        )
        
    
    async def signup_user(self, session: AsyncSession, user_data: schemas.UserCreate) -> schemas.UserOut:
        # existing_user = await user_service.get_by_email(session, user_data.email)
        # if existing_user:
        #     raise custom_exceptions.ConflictException("Email already registered", {"user_email": user_data.email} )

        # Create user model
        new_user = await user_service.create_user(session, user_data)

        logger.info(f"[AUTH] New user registered - {new_user.email}")
        # return schemas.UserOut.model_validate(new_user)
        return new_user
    
    
    def create_token_for_user(self, user: schemas.UserOut) -> str:
        token_data = {"sub": user.email}
        return security.create_access_token(token_data)




auth_service = AuthService()
