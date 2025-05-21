#rbac/service.py

from typing import List
from uuid import UUID
from user_service.rbac import models, schemas
from user_service.user.models import UserModel
from user_service.user.schemas import UserRead
from user_service.common.exceptions import custom_exceptions
from datetime import datetime


class RBACService:

    # ========== PERMISSIONS ==========

    async def create_permission(self, conn, data: schemas.PermissionCreate) -> models.PermissionModel:
        permission = models.PermissionModel(**data.dict())
        await permission.insert(conn=conn)
        return permission

    async def get_all_permissions(self, conn) -> List[models.PermissionModel]:
        return await models.PermissionModel.select(conn=conn)

    # ========== ROLES ==========

    async def create_role(self, conn, data: schemas.RoleCreate) -> models.RoleModel:
        role = models.RoleModel(name=data.name, description=data.description)
        await role.insert(conn=conn)

        # Assign permissions via pivot
        if data.permission_ids:
            permissions = await models.PermissionModel.select(
                conn=conn,
                where={"id": {"$in": data.permission_ids}}
            )
            if len(permissions) != len(data.permission_ids):
                raise custom_exceptions.BadRequestException("One or more permissions not found")

            for perm_id in data.permission_ids:
                await models.RolePermissionModel(role_id=role.id, permission_id=perm_id).insert(conn=conn)

        return role

    async def get_all_roles(self, conn) -> List[models.RoleModel]:
        return await models.RoleModel.select(conn=conn)

    async def update_role(
        self, 
        conn, 
        role_id: UUID, 
        data: schemas.RoleUpdate
    ) -> models.RoleModel:
        # 1. Fetch the role (or fail)
        role = await models.RoleModel.get(conn=conn, id=role_id)
        if not role:
            raise custom_exceptions.NotFoundException("Role not found")

        # 2. Apply non-permission updates
        update_data = data.dict(exclude_unset=True, exclude={"permission_ids"})
        for key, value in update_data.items():
            setattr(role, key, value)

        # 3. Handle permission updates (if provided)
        if hasattr(data, "permission_ids") and data.permission_ids is not None:
            # Fetch all permissions one-by-one (FastORM doesn't support bulk WHERE IN)
            missing_perms = []
            valid_perms = []
            
            for perm_id in data.permission_ids:
                perm = await models.PermissionModel.get(conn=conn, id=perm_id)
                if perm:
                    valid_perms.append(perm_id)
                else:
                    missing_perms.append(str(perm_id))  # Convert UUID to string for error message
            
            if missing_perms:
                raise custom_exceptions.BadRequestException(
                    f"Permissions not found: {', '.join(missing_perms)}"
                )

            # Atomic update: Delete old + insert new
            try:
                # Delete old permissions (FastORM-compatible way)
                existing = await models.RolePermissionModel.select(conn=conn, role_id=role_id)
                for record in existing:
                    await record.delete(conn=conn)

                # Insert new permissions
                for perm_id in valid_perms:
                    await models.RolePermissionModel(
                        role_id=role_id,
                        permission_id=perm_id
                    ).insert(conn=conn)
                    
            except Exception as e:
                raise custom_exceptions.DatabaseException("Failed to update permissions")

        # 4. Save role updates
        await role.update(conn=conn)
        
        return role

    # ========== USER ROLE ASSIGNMENT ==========

    async def assign_roles_to_user(self, conn, user_id: UUID, role_ids: List[UUID]) -> UserRead:
        user = await UserModel.get(conn=conn, where={"id": user_id})
        if not user:
            raise custom_exceptions.NotFoundException("User not found")

        roles = await models.RoleModel.select(conn=conn, where={"id": {"$in": role_ids}})
        if len(roles) != len(role_ids):
            raise custom_exceptions.BadRequestException("One or more roles not found")

        for role_id in role_ids:
            await models.UserRoleModel(user_id=user_id, role_id=role_id).insert(conn=conn)

        # Populate roles manually for response
        roles_out = [schemas.RoleRead.model_validate(role) for role in roles]
        user_out = UserRead.model_validate(user)
        user_out.roles = roles_out
        return user_out

rbac_service = RBACService()



# # rbac/service.py

# from typing import List
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select
# from user_service.db import DBSessionDep
# from user_service.rbac import models, schemas
# from user_service.user.models import UserModel
# from user_service.user.schemas import  UserRead
# from user_service.common.exceptions import custom_exceptions
# from uuid import UUID

# class RBACService:
#     def __init__(self, db: DBSessionDep):
#         self.db = db

#     # ========== PERMISSIONS ==========

#     async def create_permission(self, data: schemas.PermissionCreate) -> models.PermissionModel:
#         permission = models.PermissionModel(**data.dict())
#         self.db.add(permission)
#         await self.db.commit()
#         await self.db.refresh(permission)
#         return permission

#     async def get_all_permissions(self) -> List[models.PermissionModel]:
#         result = await self.db.execute(select(models.PermissionModel))
#         return result.scalars().all()

#     # ========== ROLES ==========

#     async def create_role(self, data: schemas.RoleCreate) -> models.RoleModel:
#         role = models.RoleModel(name=data.name, description=data.description)

#         if data.permission_ids:
#             permissions = await self.db.execute(
#                 select(models.PermissionModel).where(models.PermissionModel.id.in_(data.permission_ids))
#             )
#             permission_list = permissions.scalars().all()

#             if len(permission_list) != len(data.permission_ids):
#                 raise custom_exceptions.BadRequestException("One or more permissions not found")

#             role.permissions = permission_list

#         self.db.add(role)
#         await self.db.commit()
#         await self.db.refresh(role)
#         return role

#     async def get_all_roles(self) -> List[models.RoleModel]:
#         result = await self.db.execute(select(models.RoleModel))
#         return result.scalars().all()

#     async def update_role(self, role_id: str, data: schemas.RoleUpdate) -> models.RoleModel:
#         result = await self.db.execute(select(models.RoleModel).where(models.RoleModel.id == role_id))
#         role = result.scalar_one_or_none()
#         if not role:
#             raise custom_exceptions.NotFoundException("Role not found")

#         if data.name:
#             role.name = data.name
#         if data.description:
#             role.description = data.description
#         if data.permission_ids is not None:
#             permissions = await self.db.execute(
#                 select(models.PermissionModel).where(models.PermissionModel.id.in_(data.permission_ids))
#             )
#             permission_list = permissions.scalars().all()
#             if len(permission_list) != len(data.permission_ids):
#                 raise custom_exceptions.BadRequestException("Invalid permissions provided")
#             role.permissions = permission_list

#         await self.db.commit()
#         await self.db.refresh(role)
#         return role

#     # ========== USER ROLE ASSIGNMENT ==========

#     async def assign_roles_to_user(self, user_id: UUID, role_ids: List[UUID]) -> UserModel:
#         result = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
#         user = result.scalar_one_or_none()
#         if not user:
#             raise custom_exceptions.NotFoundException("User not found")

#         result = await self.db.execute(
#             select(models.RoleModel).where(models.RoleModel.id.in_(role_ids))
#         )
#         roles = result.scalars().all()
#         if len(roles) != len(role_ids):
#             raise custom_exceptions.BadRequestException("One or more roles not found")

#         user.roles = roles
#         await self.db.commit()
#         await self.db.refresh(user)
#         # return user
#         return UserRead.from_orm(user)

