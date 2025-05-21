# common/exceptions/custom_exceptions.py

from typing import Optional, Dict
from fastapi import status
from . import AppException


class BadRequestException(AppException):
    def __init__(self, message="Bad request", payload: Optional[Dict]=None):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, "bad_request", payload)


class UnauthorizedException(AppException):
    def __init__(self, message="Unauthorized", payload: Optional[Dict]=None):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED, "unauthorized", payload)


class ForbiddenException(AppException):
    def __init__(self, message="Forbidden", payload: Optional[Dict]=None):
        super().__init__(message, status.HTTP_403_FORBIDDEN, "forbidden", payload)


class NotFoundException(AppException):
    def __init__(self, message="Resource not found", payload: Optional[Dict]=None):
        super().__init__(message, status.HTTP_404_NOT_FOUND, "not_found", payload)


class ConflictException(AppException):
    def __init__(self, message="Conflict", payload: Optional[Dict]=None):
        super().__init__(message, status.HTTP_409_CONFLICT, "conflict", payload)


class UnprocessableException(AppException):
    def __init__(self, message="Unprocessable entity", payload: Optional[Dict]=None):
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_ENTITY, "unprocessable", payload)


class InternalServerException(AppException):
    def __init__(self, message="Internal server error", payload: Optional[Dict]=None):
        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR, "internal_error", payload)


class DatabaseException(AppException):
    def __init__(self, message="Database operation failed", payload: Optional[Dict] = None):
        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR, "database_error", payload)
