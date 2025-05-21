# common/logging.py

import logging
import sys
import json
from datetime import datetime
from typing import Any, Dict
from user_service.core import settings

# Define sensitive keys to redact
SENSITIVE_KEYS = {key.lower() for key in settings.SENSITIVE_KEYS}



def redact_value(key: str, value: Any) -> Any:
    """Redact sensitive values based on key match, unless in debug mode."""
    if settings.DEBUG_MODE:
        return value  # Don't redact anything in debug mode
    if key.lower() in SENSITIVE_KEYS:
        return "***REDACTED***"
    return value

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        # Base log record
        log_record: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "service": settings.PROJECT_NAME,
            "environment": settings.ENVIRONMENT,
            "source_module": record.module,
            "source_function": record.funcName,
            "line": record.lineno,
            "message": record.getMessage(),
        }

        # Add any custom attributes passed via `extra`
        standard_attrs = {
            'name', 'msg', 'args', 'levelname', 'levelno', 'pathname', 'filename',
            'module', 'exc_info', 'exc_text', 'stack_info', 'lineno', 'funcName',
            'created', 'msecs', 'relativeCreated', 'thread', 'threadName', 'processName',
            'process', 'message'
        }

        for key, value in record.__dict__.items():
            if key not in standard_attrs:
                log_record[key] = redact_value(key, value)

        return json.dumps(log_record, indent=2, ensure_ascii=False)


class LogConfigurator:
    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(settings.LOG_LEVEL.upper())

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())

        self.logger.handlers.clear()
        self.logger.addHandler(handler)

    def get_logger(self, name: str = None) -> logging.Logger:
        return self.logger if name is None else logging.getLogger(name)


# Configure logging globally at import time
LogConfigurator()
logger = logging.getLogger("user_service")
