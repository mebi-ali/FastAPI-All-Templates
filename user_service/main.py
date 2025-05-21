from fastapi import FastAPI
from user_service.core import settings 
from user_service.common import logger
from user_service.common import register_exception_handlers
from user_service.db import db_manager
from user_service.api.v1 import api_v1_router


app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG_MODE,
)

register_exception_handlers(app)


# Mount the entire v1 API
app.include_router(api_v1_router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    logger.info(f"🔧 Environment: {settings.ENVIRONMENT}")
    await db_manager.test_connection()


@app.get("/")
def read_root():
    return {"msg": "Hello from User Service!"}

@app.get("/health", tags=["Health"])
async def healthcheck():
    return {"status": "ok"}