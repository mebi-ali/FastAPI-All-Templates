#user/schemas.py

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    full_name: str = Field(..., max_length=100)
    email: EmailStr
    dob: date
    gender: Optional[str] = Field(None, max_length=10)
    marketing_check: bool = False
    


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=256)


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=100)
    dob: Optional[date] = None
    gender: Optional[str] = Field(None, max_length=10)
    marketing_check: Optional[bool] = True
    is_active: Optional[bool] = True
    is_verified: Optional[bool] = True
    is_superuser: Optional[bool] = False

# Response Schema External Use
class UserOut(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
      orm = True

# User Filters
class UserFilters(BaseModel):
    is_deleted: Optional[bool] = Field(None, description="Filter by deletion status")
    is_active: Optional[bool] = Field(None, description="Filter by active status")
    is_verified: Optional[bool] = Field(None, description="Filter by verification status")
    email_contains: Optional[str] = Field(None, description="Filter by email substring")



# class UserOut(BaseModel):
#     id: UUID
#     full_name: Optional[str]
#     email: Optional[EmailStr]
#     dob: Optional[date]
#     gender: Optional[str]
#     marketing_check: bool
#     is_active: bool
#     is_verified: bool
#     is_superuser: bool
#     last_login: Optional[datetime]
#     created_at: datetime
#     updated_at: datetime

#     class Config:
#         orm_mode = True

