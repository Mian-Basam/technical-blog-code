# repository.py
from schemas import Book, BookCreate, BookUpdate


class BookRepository:
    def __init__(self) -> None:
        self._books: dict[int, Book] = {}
        self._next_id = 1

    def list(self, limit: int, offset: int, author: str | None) -> tuple[list[Book], int]:
        books = list(self._books.values())
        if author:
            books = [b for b in books if author.lower() in b.author.lower()]
        return books[offset : offset + limit], len(books)

    def get(self, book_id: int) -> Book | None:
        return self._books.get(book_id)

    def create(self, data: BookCreate) -> Book:
        book = Book(id=self._next_id, **data.model_dump())
        self._books[book.id] = book
        self._next_id += 1
        return book

    def update(self, book_id: int, data: BookUpdate) -> Book | None:
        book = self._books.get(book_id)
        if book is None:
            return None
        changes = data.model_dump(exclude_unset=True)
        updated = book.model_copy(update=changes)
        self._books[book_id] = updated
        return updated

    def delete(self, book_id: int) -> bool:
        return self._books.pop(book_id, None) is not None
