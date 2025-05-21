#user/schemas.py

from datetime import date, datetime
from typing import Optional, List
from uuid import UUID
from user_service.rbac.schemas import RoleRead
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    full_name: str = Field(..., max_length=100)
    email: EmailStr
    dob: date
    gender: Optional[str] = Field(None, max_length=10)
    marketing_check: bool = False


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=256)
    role_ids: Optional[List[UUID]] = Field(default_factory=list)


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=100)
    dob: Optional[date] = None
    gender: Optional[str] = Field(None, max_length=10)
    marketing_check: Optional[bool] = True
    is_active: Optional[bool] = True
    is_verified: Optional[bool] = True
    is_superuser: Optional[bool] = False


class UserOut(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None


class UserRead(UserOut):
    roles: List[RoleRead] = []

    class Config:
        from_attributes = True


class UserFilters(BaseModel):
    is_deleted: Optional[bool] = Field(None, description="Filter by deletion status")
    is_active: Optional[bool] = Field(None, description="Filter by active status")
    is_verified: Optional[bool] = Field(None, description="Filter by verification status")
    email_contains: Optional[str] = Field(None, description="Filter by email substring")

