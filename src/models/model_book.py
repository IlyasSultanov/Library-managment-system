"""
Model for the book table.

This module provides the model for the book table.
"""

from src.db.base_class import BaseModel
from sqlalchemy.orm import mapped_column, Mapped


class Book(BaseModel):
    """ """

    __tablename__ = "books"

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
