# rbac/schemas.py

from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import UUID


# ===== Permission Schemas =====

class PermissionBase(BaseModel):
    name: str = Field(..., example="create_user")
    description: Optional[str] = Field(None, example="Allows creating a new user")


class PermissionCreate(PermissionBase):
    pass


class PermissionRead(PermissionBase):
    id: UUID

    class Config:
        from_attributes = True  # ✅ Required for from_orm()
        

# ===== Role Schemas =====

class RoleBase(BaseModel):
    name: str = Field(..., example="admin")
    description: Optional[str] = Field(None, example="Administrator with full access")


class RoleCreate(RoleBase):
    permission_ids: Optional[List[UUID]] = Field(default_factory=list)


class RoleUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    permission_ids: Optional[List[UUID]] = Field(default_factory=list)


class RoleRead(RoleBase):
    id: UUID
    permissions: List[PermissionRead] = Field(default_factory=list)

    class Config:
        from_attributes = True  # ✅ Required for from_orm()


# ===== User Role Association =====

class UserRoleAssignment(BaseModel):
    user_id: UUID
    role_ids: List[UUID]


class UserRoleRead(BaseModel):
    user_id: UUID
    roles: List[RoleRead]

    class Config:
        from_attributes = True  # ✅ Optional if used with from_orm()







# #rbac/schemas.py

# from typing import Optional, List
# from pydantic import BaseModel, Field
# from uuid import UUID


# # ===== Permission Schemas =====

# class PermissionBase(BaseModel):
#     name: str = Field(..., example="create_user")
#     description: Optional[str] = Field(None, example="Allows creating a new user")


# class PermissionCreate(PermissionBase):
#     pass


# class PermissionRead(PermissionBase):
#     id: UUID


# # ===== Role Schemas =====

# class RoleBase(BaseModel):
#     name: str = Field(..., example="admin")
#     description: Optional[str] = Field(None, example="Administrator with full access")


# class RoleCreate(RoleBase):
#     permission_ids: Optional[List[UUID]] = Field(default_factory=list)


# class RoleUpdate(BaseModel):
#     name: Optional[str]
#     description: Optional[str]
#     permission_ids: Optional[List[UUID]] = Field(default_factory=list)


# class RoleRead(RoleBase):
#     id: UUID
#     permissions: List[PermissionRead] = Field(default_factory=list)


# # ===== User Role Association =====

# class UserRoleAssignment(BaseModel):
#     user_id: UUID
#     role_ids: List[UUID]


# class UserRoleRead(BaseModel):
#     user_id: UUID
#     roles: List[RoleRead]
