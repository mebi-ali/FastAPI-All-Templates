from fastapi import FastAPI
from user_service.core import settings 
from user_service.common import logger
from user_service.common import register_exception_handlers
from user_service.db import db_manager

app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG_MODE,
)

register_exception_handlers(app)

@app.on_event("startup")
async def startup_event():
    logger.info(f"🔧 Environment: {settings.ENVIRONMENT}")
    await db_manager.test_connection()


@app.get("/")
def read_root():
    return {"msg": "Hello from User Service!"}