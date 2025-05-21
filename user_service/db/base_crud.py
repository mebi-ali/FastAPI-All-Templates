#db/base_crud.py

from uuid import UUID
from datetime import datetime
from typing import Type, TypeVar, Generic, Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, and_, update as sql_update, delete as sql_delete
from sqlalchemy.exc import SQLAlchemyError
from user_service.common import logger, custom_exceptions 


ModelType = TypeVar("ModelType")


class BaseCRUD(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_by_id(self, session: AsyncSession, obj_id: UUID) -> ModelType:
        try:
            logger.debug(f"[CRUD] Getting {self.model.__name__} by ID: {obj_id}")
            stmt = select(self.model).where(self.model.id == obj_id, self.model.is_deleted==False)
            result = await session.execute(stmt)
            obj = result.scalar_one_or_none()
            if obj is None:
                # raise custom_exceptions.NotFoundException(f"User not found.", {"user_id": str(obj_id)})
                raise custom_exceptions.NotFoundException(f"{self.model.__name__} with id={obj_id} not found")
            return obj
        except SQLAlchemyError as e:
            raise custom_exceptions.DatabaseException(f"[GET] Error retrieving {self.model.__name__} by id: {e}")


    async def get_all(
        self,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        filters: dict = None
    ) -> List[ModelType]:
        try:
            logger.debug(f"[CRUD] Getting all {self.model.__name__} records (skip={skip}, limit={limit}, filters={filters})")

            stmt = select(self.model).options(selectinload(self.model.roles))
            if filters:
                conditions = []
                for key, value in filters.items():
                    if value is None:
                        continue  # Skip empty filters
                    if key == "email_contains":
                        conditions.append(self.model.email.ilike(f"%{value}%"))
                    else:
                        column_attr = getattr(self.model, key, None)
                        if column_attr is not None:
                            conditions.append(column_attr == value)
                stmt = stmt.where(and_(*conditions))

            stmt = stmt.offset(skip).limit(limit)

            result = await session.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise custom_exceptions.DatabaseException(f"[LIST] Error retrieving all {self.model.__name__}: {e}")
        

    async def create(self, session: AsyncSession, obj_data: Dict[str, Any]) -> ModelType:
        try:
            logger.debug(f"[CRUD] Creating {self.model.__name__} with data: {obj_data}")
            db_obj = self.model(**obj_data)
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            await session.rollback()
            raise custom_exceptions.DatabaseException(f"[CREATE] Error creating {self.model.__name__}: {e}")

    async def update(self, session: AsyncSession, obj_id: UUID, update_data: Dict[str, Any]) -> ModelType:
        try:
            logger.debug(f"[CRUD] Updating {self.model.__name__} id={obj_id} with data: {update_data}")
            stmt = (
                sql_update(self.model)
                .where(self.model.id == obj_id)
                .values(**update_data)
                .execution_options(synchronize_session="fetch")
            )
            result = await session.execute(stmt)
            await session.commit()

            # Check if any row was updated
            if result.rowcount == 0:
                raise custom_exceptions.NotFoundException(f"{self.model.__name__} with id={obj_id} not found for update")

            return await self.get_by_id(session, obj_id)
        except SQLAlchemyError as e:
            await session.rollback()
            raise custom_exceptions.DatabaseException(f"[UPDATE] Error updating {self.model.__name__} with id={obj_id}: {e}")

    async def delete(self, session: AsyncSession, obj_id: UUID) -> bool:
        try:
            logger.debug(f"[CRUD] Soft deleting {self.model.__name__} with id={obj_id}")
            
            stmt = (
                sql_update(self.model)
                .where(self.model.id == obj_id, self.model.is_deleted == False)
                .values(
                    is_deleted=True,
                    deleted_at=datetime.utcnow()
                )
            )
            result = await session.execute(stmt)
            await session.commit()

            if result.rowcount == 0:
                raise custom_exceptions.NotFoundException(
                    f"{self.model.__name__} with id={obj_id} not found or already deleted"
                )

            return True
        except SQLAlchemyError as e:
            await session.rollback()
            raise custom_exceptions.DatabaseException(
                f"[SOFT DELETE] Error deleting {self.model.__name__} with id={obj_id}: {e}"
            )