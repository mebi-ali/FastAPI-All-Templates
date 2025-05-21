# common/exceptions/base.py

import inspect
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
            "error_message": self.message,
            "payload": self.payload,
        }

        if log:
            # 🧠 Walk the stack until we're outside of common.exceptions
            caller_frame_info = None
            for frame_info in inspect.stack():
                module_name = frame_info.frame.f_globals.get("__name__", "")
                if not module_name.startswith("user_service.common.exceptions"):
                    caller_frame_info = frame_info
                    break

            logger.error(
                self.message,
                extra={
                    "error_code": self.error_code,
                    "payload": self.payload,
                    "status_code": status_code,
                    "source_module": caller_frame_info.frame.f_globals.get("__name__", "unknown") if caller_frame_info else "unknown",
                    "source_function": caller_frame_info.function if caller_frame_info else "unknown",
                    "line": caller_frame_info.lineno if caller_frame_info else -1,
                },
            )

        super().__init__(status_code=status_code, detail=detail)
