# schemas.py
from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    year: int = Field(..., ge=1450, le=2100)
    isbn: str | None = Field(default=None, pattern=r"^\d{10}(\d{3})?$")


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    author: str | None = Field(default=None, min_length=1, max_length=100)
    year: int | None = Field(default=None, ge=1450, le=2100)
    isbn: str | None = Field(default=None, pattern=r"^\d{10}(\d{3})?$")


class Book(BookCreate):
    id: int


class BookPage(BaseModel):
    items: list[Book]
    total: int
    limit: int
    offset: int
