from fastapi import APIRouter
from src.endpoint.endpoint import router as crud_book_router

router = APIRouter(prefix="/api", tags=["API"])

router.include_router(router=crud_book_router)
