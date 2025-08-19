"""
Endpoints for the book table.

This module provides the endpoints for the book table.
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.schemas.book_schemas import BookCreate, BookUpdate, BookResponse
from src.service.crud import book

router = APIRouter(prefix="/books", tags=["books"])


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book_in: BookCreate, db: AsyncSession = Depends(get_db)):
    return await book.create(db=db, obj_in=book_in)


@router.get("/{book_id}", response_model=BookResponse)
async def read_book(book_id: UUID, db: AsyncSession = Depends(get_db)):
    obj = await book.get(db, book_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Book not found")
    return obj


@router.get("/", response_model=list[BookResponse])
async def read_books(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    search: str = Query(None, description="Search by name"),
):
    return await book.get_multi(db, skip=skip, limit=limit, search=search)


@router.patch("/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: UUID, book_in: BookUpdate, db: AsyncSession = Depends(get_db)
):
    obj = await book.get(db, book_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Book not found")
    return await book.update(db=db, db_obj=obj, obj_in=book_in)


@router.delete("/{book_id}", status_code=200)
async def delete_book(book_id: UUID, db: AsyncSession = Depends(get_db)):
    obj = await book.remove(db=db, book_id=book_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Book not found or already deleted")
    return {"status": "deleted", "id": obj.id, "deleted_at": obj.deleted_at}
