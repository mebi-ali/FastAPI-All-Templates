# db/database.py

from typing import AsyncGenerator, Annotated
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from fastapi import Depends
from sqlalchemy import text

from user_service.core import settings
from user_service.common import logger
from user_service.common import custom_exceptions


class DatabaseManager:
    def __init__(self):
        self.engine = create_async_engine(
            settings.DATABASE_URL,
            echo=settings.DEBUG_MODE,  # If you want less logs change DEBUG_MODE=False
            future=True,
            pool_pre_ping=True,
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            try:
                yield session
            except Exception as e:
                logger.exception("❌ Database session error")
                raise custom_exceptions.InternalServerException(
                    message="Database session failure",
                    payload={"exception": str(e)}
                )
            finally:
                await session.close()

    async def test_connection(self):
        try:
            async with self.engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            logger.info("✅ Successfully connected to the database.")
        except Exception as e:
            logger.exception("❌ Failed to connect to the database")
            raise custom_exceptions.InternalServerException(
                message="Database connection failed",
                payload={"exception": str(e)}
            )


# Single instance used throughout the app
db_manager = DatabaseManager()

# FastAPI-compatible dependency
DBSessionDep = Annotated[AsyncSession, Depends(db_manager.get_session)]
