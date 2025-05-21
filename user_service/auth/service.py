# user_service/auth/service.py

from datetime import datetime, timedelta

from user_service.auth.schemas import LoginRequest, LoginResponse
from user_service.user.models import UserModel
from user_service.core import security
from user_service.user import user_service, schemas
from user_service.common import custom_exceptions, logger


class AuthService:
    async def authenticate_user(self, conn, login_data: LoginRequest) -> LoginResponse:
        logger.debug(f"[AUTH] Authenticating user: {login_data.email}")

        user = await UserModel.get(conn=conn, email=login_data.email, is_deleted=False)
        if not user:
            raise custom_exceptions.UnauthorizedException("Invalid credentials")

        if not security.verify_password(login_data.password, user.password):
            raise custom_exceptions.UnauthorizedException("Invalid credentials")

        if not user.is_verified:
            raise custom_exceptions.UnauthorizedException("Please verify your email to proceed")
        if not user.is_active or user.is_deleted:
            raise custom_exceptions.UnauthorizedException("Account is inactive or deleted")

        token_data = {"sub": user.email}
        access_token = security.create_access_token(token_data)
        expires_at = datetime.utcnow() + timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)

        logger.info(f"[AUTH] User logged in successfully - {user.email}")

        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            expires_at=expires_at
    )
    

    async def signup_user(self, conn, user_data: schemas.UserCreate) -> schemas.UserOut:
        # Check for existing user (optional)
        existing_user = None
        try:
            existing_user = await user_service.get_by_email(conn, user_data.email)
        except custom_exceptions.NotFoundException:
            pass

        if existing_user:
            raise custom_exceptions.ConflictException("Email already registered", {"user_email": user_data.email})

        new_user = await user_service.create_user(conn, user_data)
        logger.info(f"[AUTH] New user registered - {new_user.email}")
        return new_user

    def create_token_for_user(self, user: schemas.UserOut) -> str:
        token_data = {"sub": user.email}
        return security.create_access_token(token_data)


# Singleton
auth_service = AuthService()

