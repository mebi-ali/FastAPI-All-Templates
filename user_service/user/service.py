
from uuid import UUID, uuid4
from typing import Optional, List
from pydantic import EmailStr
from datetime import datetime

from user_service.user.models import UserModel
from user_service.user.schemas import UserCreate, UserUpdate, UserFilters
from user_service.core import get_password_hash, verify_password
from user_service.common import custom_exceptions, logger


class UserService:

    async def get_user_by_id(self, conn, user_id: UUID) -> UserModel:
        logger.debug(f"[UserService] Getting user by ID: {user_id}")
        user = await UserModel.get(conn=conn, id=user_id, is_deleted=False)
        if not user:
            raise custom_exceptions.NotFoundException("User not found", {"user_id": user_id})
        return user

    async def get_all_users(
        self,
        conn,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[UserFilters] = None,
    ) -> List[UserModel]:
        logger.debug(f"[UserService] Getting all users (skip={skip}, limit={limit}, filters={filters})")

        filters_dict = filters.dict(exclude_unset=True) if filters else {}
        filters_dict = {k: v for k, v in filters_dict.items() if v is not None}

        if "email_contains" in filters_dict:
            filters_dict["email__ilike"] = f"%{filters_dict.pop('email_contains')}%"

        users = await UserModel.select(conn=conn, **filters_dict)
        return users[skip: skip + limit]

    async def get_by_email(self, conn, email: EmailStr) -> UserModel:
        logger.debug(f"[UserService] Fetching user by email: {email}")
        user = await UserModel.get(conn=conn, email=email, is_deleted=False)
        if not user:
            raise custom_exceptions.NotFoundException("User not found", {"user_email": email})
        return user

    async def create_user(self, conn, user_in: UserCreate) -> UserModel:
        logger.debug(f"[UserService] Creating user: {user_in.email}")

        user_dict = user_in.dict(exclude={"role_ids"})
        user_dict["id"] = uuid4()
        user_dict["password"] = get_password_hash(user_in.password)
        now = datetime.utcnow()
        user_dict["created_at"] = now
        user_dict["updated_at"] = now

        user = UserModel(**user_dict)
        await user.insert(conn=conn)

        # Note: role_ids ignored intentionally
        return user

    async def update_user(self, conn, user_id: UUID, user_in: UserUpdate) -> UserModel:
        logger.debug(f"[UserService] Updating user ID: {user_id}")
        user = await UserModel.get(conn=conn, id=user_id, is_deleted=False)
        if not user:
            raise custom_exceptions.NotFoundException("User not found", {"user_id": user_id})

        update_data = user_in.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()

        for key, value in update_data.items():
            setattr(user, key, value)

        await user.update(conn=conn)
        return user

    async def delete_user(self, conn, user_id: UUID) -> bool:
        logger.debug(f"[UserService] Deleting user ID: {user_id}")
        user = await self.get_user_by_id(conn, user_id)
        user.is_deleted = True
        user.updated_at = datetime.utcnow()
        await user.update(conn=conn)
        return True

    async def update_password(
        self,
        conn,
        user_id: UUID,
        new_password: str,
        old_password: Optional[str] = None,
        verify_old: bool = False,
    ) -> UserModel:
        logger.debug(f"[UserService] Updating password for user ID: {user_id}")
        user = await self.get_user_by_id(conn, user_id)

        if verify_old and old_password:
            if not verify_password(old_password, user.password):
                raise custom_exceptions.UnauthorizedException("Old password is incorrect")

        user.password = get_password_hash(new_password)
        user.updated_at = datetime.utcnow()
        await user.update(conn=conn)
        return user


# Singleton instance
user_service = UserService()


