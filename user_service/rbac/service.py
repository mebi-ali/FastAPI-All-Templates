# rbac/service.py

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from user_service.db import DBSessionDep
from user_service.rbac import models, schemas
from user_service.user.models import UserModel
from user_service.user.schemas import  UserRead
from user_service.common.exceptions import custom_exceptions
from uuid import UUID

class RBACService:
    def __init__(self, db: DBSessionDep):
        self.db = db

    # ========== PERMISSIONS ==========

    async def create_permission(self, data: schemas.PermissionCreate) -> models.PermissionModel:
        permission = models.PermissionModel(**data.dict())
        self.db.add(permission)
        await self.db.commit()
        await self.db.refresh(permission)
        return permission

    async def get_all_permissions(self) -> List[models.PermissionModel]:
        result = await self.db.execute(select(models.PermissionModel))
        return result.scalars().all()

    # ========== ROLES ==========

    async def create_role(self, data: schemas.RoleCreate) -> models.RoleModel:
        role = models.RoleModel(name=data.name, description=data.description)

        if data.permission_ids:
            permissions = await self.db.execute(
                select(models.PermissionModel).where(models.PermissionModel.id.in_(data.permission_ids))
            )
            permission_list = permissions.scalars().all()

            if len(permission_list) != len(data.permission_ids):
                raise custom_exceptions.BadRequestException("One or more permissions not found")

            role.permissions = permission_list

        self.db.add(role)
        await self.db.commit()
        await self.db.refresh(role)
        return role

    async def get_all_roles(self) -> List[models.RoleModel]:
        result = await self.db.execute(select(models.RoleModel))
        return result.scalars().all()

    async def update_role(self, role_id: str, data: schemas.RoleUpdate) -> models.RoleModel:
        result = await self.db.execute(select(models.RoleModel).where(models.RoleModel.id == role_id))
        role = result.scalar_one_or_none()
        if not role:
            raise custom_exceptions.NotFoundException("Role not found")

        if data.name:
            role.name = data.name
        if data.description:
            role.description = data.description
        if data.permission_ids is not None:
            permissions = await self.db.execute(
                select(models.PermissionModel).where(models.PermissionModel.id.in_(data.permission_ids))
            )
            permission_list = permissions.scalars().all()
            if len(permission_list) != len(data.permission_ids):
                raise custom_exceptions.BadRequestException("Invalid permissions provided")
            role.permissions = permission_list

        await self.db.commit()
        await self.db.refresh(role)
        return role

    # ========== USER ROLE ASSIGNMENT ==========

    async def assign_roles_to_user(self, user_id: UUID, role_ids: List[UUID]) -> UserModel:
        result = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise custom_exceptions.NotFoundException("User not found")

        result = await self.db.execute(
            select(models.RoleModel).where(models.RoleModel.id.in_(role_ids))
        )
        roles = result.scalars().all()
        if len(roles) != len(role_ids):
            raise custom_exceptions.BadRequestException("One or more roles not found")

        user.roles = roles
        await self.db.commit()
        await self.db.refresh(user)
        # return user
        return UserRead.from_orm(user)

