# main.py
from fastapi import Depends, FastAPI, HTTPException, Query, status

from repository import BookRepository
from schemas import Book, BookCreate, BookPage, BookUpdate

app = FastAPI(title="Books API", version="1.0.0")
_repo = BookRepository()


def get_repo() -> BookRepository:
    return _repo


def get_book_or_404(book_id: int, repo: BookRepository = Depends(get_repo)) -> Book:
    book = repo.get(book_id)
    if book is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Book {book_id} not found")
    return book

@app.get("/books", response_model=BookPage)
def list_books(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    author: str | None = None,
    repo: BookRepository = Depends(get_repo),
):
    items, total = repo.list(limit, offset, author)
    return BookPage(items=items, total=total, limit=limit, offset=offset)


@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(data: BookCreate, repo: BookRepository = Depends(get_repo)):
    return repo.create(data)


@app.get("/books/{book_id}", response_model=Book)
def get_book(book: Book = Depends(get_book_or_404)):
    return book


@app.patch("/books/{book_id}", response_model=Book)
def update_book(
    data: BookUpdate,
    book: Book = Depends(get_book_or_404),
    repo: BookRepository = Depends(get_repo),
):
    return repo.update(book.id, data)


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book: Book = Depends(get_book_or_404), repo: BookRepository = Depends(get_repo)):
    repo.delete(book.id)
