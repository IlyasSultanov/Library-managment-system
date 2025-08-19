"""
CRUD operations for the book table.

This module provides the CRUD operations for the book table.
"""

from uuid import UUID
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only

from src.models.model_book import Book
from src.schemas.book_schemas import BookUpdate, BookCreate


class CRUDBook:
    async def get(
        self, db: AsyncSession, book_id: UUID, fileds: Optional[list[str]] = None
    ) -> Optional[Book]:
        """Get a single book by ID."""
        query = select(Book).where(Book.id == book_id)
        if fileds:
            query = query.options(
                load_only(*[getattr(Book, filed) for filed in fileds])
            )
        result = await db.execute(query)
        return result.scalars().first()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100, **filters  # type: ignore
    ) -> list[Book]:
        """Get multiple books with pagination."""
        query = (
            select(Book)
            .filter_by(**filters)
            .order_by(Book.created_at.desc())
            .offset(skip)
            .limit(limit)
        )

        result = await db.execute(query)
        return result.scalars().all()  # type: ignore

    async def create(self, db: AsyncSession, *, obj_in: BookCreate) -> Book:
        """Create a new book."""
        db_obj = Book(**obj_in.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, *, db_obj: Book, obj_in: BookUpdate
    ) -> Book:
        """Update an existing book."""
        update_data = obj_in.model_dump(exclude_unset=True)
        await db.execute(update(Book).where(Book.id == db_obj.id).values(**update_data))
        await db.commit()
        return await self.get(db, db_obj.id)

    async def remove(self, db: AsyncSession, *, book_id: UUID) -> Optional[Book]:
        """Soft delete a book (set deleted_at timestamp)."""
        try:
            book = await self.get(db, book_id)
            if not book:
                return None

            book.mark_as_deleted()
            await db.commit()
            return book
        except Exception as e:
            await db.rollback()
            raise
        finally:
            await db.close()


book = CRUDBook()
