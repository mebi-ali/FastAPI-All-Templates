from fastorm import FastORM
from typing import Optional
from uuid import UUID
from datetime import date, datetime


class UserModel(FastORM):
    _table_name = "users"
    _primary_keys = ["id"]
    _automatic_fields = ["id"]

    id: Optional[UUID]
    full_name: str
    email: str
    password: str
    dob: date
    gender: Optional[str]
    marketing_check: bool = False
    is_active: bool = True
    is_verified: bool = True
    is_superuser: bool = False
    last_login: Optional[datetime]
    is_deleted: Optional[bool] = False
    deleted_at: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
