# rbac/models.py

from typing import TYPE_CHECKING
from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from user_service.db import Base, BaseUUIDModel
import uuid
from uuid import UUID

if TYPE_CHECKING:
    from user_service.user.models import UserModel

class RoleModel(BaseUUIDModel):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)

    permissions: Mapped[list["PermissionModel"]] = relationship(
        "PermissionModel",
        secondary="role_permissions",
        back_populates="roles",
        lazy="selectin"
    )

    users: Mapped[list["UserModel"]] = relationship(
        "UserModel",
        secondary="user_roles",
        back_populates="roles",
        lazy="selectin"
    )


class PermissionModel(BaseUUIDModel):
    __tablename__ = "permissions"

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)

    roles: Mapped[list["RoleModel"]] = relationship(
        "RoleModel",
        secondary="role_permissions",
        back_populates="permissions",
        lazy="selectin"
    )


class RolePermissionModel(Base):
    __tablename__ = "role_permissions"

    role_id: Mapped[UUID] = mapped_column(ForeignKey("roles.id"), primary_key=True)
    permission_id: Mapped[UUID] = mapped_column(ForeignKey("permissions.id"), primary_key=True)


class UserRoleModel(Base):
    __tablename__ = "user_roles"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    role_id: Mapped[UUID] = mapped_column(ForeignKey("roles.id"), primary_key=True)
