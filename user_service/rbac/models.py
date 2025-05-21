# rbac/models.py

from fastorm import FastORM
from typing import Optional
from uuid import UUID


class RoleModel(FastORM):
    _table_name = "roles"
    _primary_keys = ["id"]
    _automatic_fields = ["id"]

    id: Optional[UUID]
    name: str
    description: Optional[str]


class PermissionModel(FastORM):
    _table_name = "permissions"
    _primary_keys = ["id"]
    _automatic_fields = ["id"]

    id: Optional[UUID]
    name: str
    description: Optional[str]


class RolePermissionModel(FastORM):
    _table_name = "role_permissions"
    _primary_keys = ["role_id", "permission_id"]

    role_id: UUID
    permission_id: UUID


class UserRoleModel(FastORM):
    _table_name = "user_roles"
    _primary_keys = ["user_id", "role_id"]

    user_id: UUID
    role_id: UUID

