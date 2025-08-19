"""
Endpoint for CRUD operations on books.

This module provides endpoints for creating, reading, updating, and deleting books.

Endpoints:
- POST /create: Create a new book
- GET /{book_id}: Get a book by ID
- GET /: Get all books
- PUT /{book_id}: Update a book by ID
- DELETE /{book_id}: Delete a book by ID
"""

from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.db import DepSession
from src.service.crud import book
from src.schemas.book_schemas import BookCreate, BookUpdate, BookResponse

router = APIRouter(prefix="/crud", tags=["CRUD"])


@router.post("/create", response_model=BookResponse, status_code=201)
async def create_book(
    *, db: AsyncSession = DepSession, book_in: BookCreate
) -> BookResponse:
    try:
        return await book.create(db, obj_in=book_in)
    except:
        raise HTTPException(status_code=400, detail="Could not create book")


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(*, db: AsyncSession = DepSession, book_id: UUID) -> BookResponse:
    try:
        return await book.get(db, book_id=book_id)
    except:
        raise HTTPException(status_code=404, detail="Book not found")


@router.get("/", response_model=list[BookResponse])
async def read_books(
    *, db: AsyncSession = DepSession, skip: int = 0, limit: int = 100
) -> list[BookResponse]:
    return await book.get_multi(db, skip=skip, limit=limit)


@router.put("/{book_id}", response_model=BookResponse)
async def update_book(
    *, db: AsyncSession = DepSession, book_id: UUID, book_in: BookUpdate
) -> BookResponse:
    try:
        return await book.update(db, db_obj=book_id, obj_in=book_in)
    except:
        raise HTTPException(status_code=500, detail="Server error")


@router.delete("/{book_id}", response_model=BookResponse)
async def delete_book(*, db: AsyncSession = DepSession, book_id: UUID) -> BookResponse:
    try:
        return await book.remove(db, book_id=book_id)
    except:
        raise HTTPException(status_code=404, detail="Book not found")
