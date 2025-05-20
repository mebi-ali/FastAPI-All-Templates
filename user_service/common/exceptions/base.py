# common/exceptions/base.py

from typing import Optional, Dict, Any
from fastapi import status
from starlette.exceptions import HTTPException
from user_service.common.logging import logger


class AppException(HTTPException):
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        error_code: Optional[str] = None,
        payload: Optional[Dict[str, Any]] = None,
        log: bool = True,
    ):
        self.message = message
        self.error_code = error_code or "app_error"
        self.payload = payload or {}

        detail = {
            "error": self.error_code,
            "message": self.message,
            "payload": self.payload,
        }

        if log:
            logger.error(
                "Application exception raised",
                extra={
                    "error_code": self.error_code,
                    "message": self.message,
                    "payload": self.payload,
                    "status_code": status_code,
                },
            )

        super().__init__(status_code=status_code, detail=detail)
