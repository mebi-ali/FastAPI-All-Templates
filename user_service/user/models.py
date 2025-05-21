#user/models.py

from datetime import date, datetime
from typing import Optional
from sqlalchemy import String, Boolean, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column
from user_service.db import BaseUUIDModel, SoftDeleteMixin

class UserModel(BaseUUIDModel, SoftDeleteMixin):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(256), nullable=False)
    dob: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    marketing_check: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


    def __repr__(self):
        return f"<UserModel(id={self.id}, email={self.email}, active={self.is_active})>"