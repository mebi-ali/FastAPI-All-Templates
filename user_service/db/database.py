from typing import AsyncGenerator, Annotated
import asyncpg
from fastapi import Depends
from contextlib import asynccontextmanager

from user_service.core import settings
from user_service.common import logger
from user_service.common import custom_exceptions


class DatabaseManager:
    def __init__(self):
        self.database_url = settings.DATABASE_URL

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[asyncpg.Connection, None]:
        conn = None
        try:
            conn = await asyncpg.connect(self.database_url)
            yield conn
        except Exception as e:
            logger.exception("❌ Database connection error")
            raise custom_exceptions.InternalServerException(
                message="Database connection failure",
                payload={"exception": str(e)}
            )
        finally:
            if conn:
                await conn.close()

    async def test_connection(self):
        try:
            conn = await asyncpg.connect(self.database_url)
            await conn.execute("SELECT 1")
            await conn.close()
            logger.info("✅ Successfully connected to the database.")
        except Exception as e:
            logger.exception("❌ Failed to connect to the database")
            raise custom_exceptions.InternalServerException(
                message="Database connection failed",
                payload={"exception": str(e)}
            )


# Single instance used throughout the app
db_manager = DatabaseManager()

# ✅ Proper FastAPI-compatible dependency
async def get_db_conn() -> AsyncGenerator[asyncpg.Connection, None]:
    async with db_manager.get_session() as conn:
        yield conn

DBSessionDep = Annotated[asyncpg.Connection, Depends(get_db_conn)]
