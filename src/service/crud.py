"""
CRUD operations for the book table.

This module provides the CRUD operations for the book table.
"""

from uuid import UUID
from typing import Optional, List
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import and_

from src.models.model_book import Book
from src.schemas.book_schemas import BookCreate, BookUpdate


class CRUDBook:
    def __init__(self, model):
        self.model = model

    async def get(self, db: AsyncSession, book_id: UUID) -> Optional[Book]:
        query = select(self.model).where(
            and_(self.model.id == book_id, self.model.deleted_at.is_(None))
        )
        book = await db.execute(query).scalar_one_or_none()
        return book 

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
    ) -> List[Book]:
        query = select(self.model).where(self.model.deleted_at.is_(None))

        if search:
            query = query.filter(self.model.name.ilike(f"%{search}%"))

        query = query.order_by(self.model.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: BookCreate) -> Book:
        db_obj = self.model(**obj_in.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, *, db_obj: Book, obj_in: BookUpdate
    ) -> Book:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, book_id: UUID) -> Optional[Book]:
        obj = await self.get(db, book_id)
        if obj:
            obj.mark_as_deleted()
            await db.commit()
            await db.refresh(obj)
        return obj


# Использование
book = CRUDBook(model=Book)
