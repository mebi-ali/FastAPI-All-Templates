#user/service.py

from uuid import UUID

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import EmailStr

from user_service.db import BaseCRUD
from .models import UserModel
from .schemas import UserCreate, UserUpdate, UserFilters
from user_service.core import get_password_hash, verify_password
from user_service.common import custom_exceptions, logger


class UserService(BaseCRUD[UserModel]):
    def __init__(self):
        super().__init__(UserModel)

    async def get_user_by_id(self, session: AsyncSession, user_id: UUID) -> UserModel:
        logger.debug(f"[UserService] Getting user by ID: {user_id}")
        user_in = await self.get_by_id(session, user_id)
        return user_in
        
        
    async def get_all_users(
        self,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        filters: UserFilters = None
    ) -> List[UserModel]:
        logger.debug(f"[UserService] Getting all users (skip={skip}, limit={limit}, filters={filters})")
        filters_dict = filters.dict(exclude_unset=True) if filters else {}
        return await self.get_all(session, skip=skip, limit=limit, filters=filters_dict)
    # async def get_all_users(self, session: AsyncSession, skip: int = 0, limit: int = 100) -> List[UserModel]:
    #     logger.debug(f"[UserService] Getting all users (skip={skip}, limit={limit})")
    #     return await self.get_all(session, skip, limit)

    async def get_by_email(self, session: AsyncSession, email: EmailStr) -> Optional[UserModel]:
        logger.debug(f"[UserService] Fetching user by email: {email}")
        stmt = select(self.model).where(self.model.email == email, self.model.is_deleted==False)
        result = await session.execute(stmt)
        user =  result.scalar_one_or_none()
        if not user: 
            raise custom_exceptions.NotFoundException("User not found.", {"user_email": email})
        return user

    async def create_user(self, session: AsyncSession, user_in: UserCreate) -> UserModel:
        logger.debug(f"[UserService] Creating user: {user_in.email}")
        # existing_user = await self.get_by_email(session, user_in.email) We will deal with this later
        # if existing_user:
            # raise custom_exceptions.ConflictException("User with this email already exists", {"user_email": user_in.email})

        user_dict = user_in.dict()
        user_dict["password"] = get_password_hash(user_in.password)
        return await self.create(session, user_dict)

    async def update_user(self, session: AsyncSession, user_id: UUID, user_in: UserUpdate) -> UserModel:
        user = await self.get_user_by_id(session, user_id)
        if not user:
            raise custom_exceptions.NotFoundException("User not found.", {"user_id": user_id})
            
        logger.debug(f"[UserService] Updating user id={user_id}")
        update_dict = user_in.dict(exclude_unset=True)
        return await self.update(session, user_id, update_dict)

    async def delete_user(self, session: AsyncSession, user_id: UUID) -> bool:
        logger.debug(f"[UserService] Deleting user id={user_id}")
        return await self.delete(session, user_id)

    async def update_password(
        self,
        session: AsyncSession,
        user_id: UUID,
        new_password: str,
        old_password: Optional[str] = None,
        verify_old: bool = False
    ) -> UserModel:
        logger.debug(f"[UserService] Updating password for user id={user_id}")

        user = await self.get_user_by_id(session, user_id)

        # If old password verification is required (e.g., user-initiated)
        if verify_old and old_password:
            if not verify_password(old_password, user.password):
                raise custom_exceptions.UnauthorizedException("Old password is incorrect")

        hashed_password = get_password_hash(new_password)
        return await self.update(session, user_id, {"password": hashed_password})

# Singleton service instance
user_service = UserService()
