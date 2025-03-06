from fastapi import APIRouter
from typing import List
from .models import books
from .schemas import Book

router = APIRouter()


@router.get("/", response_model=List[Book])
async def get_books():
    return books


@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: int):
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        return {"error": "Book not found"}
    return book


@router.post("/", response_model=Book)
async def add_book(book: Book):
    new_book = book.dict()
    new_book["id"] = len(books) + 1
    books.append(new_book)
    return new_book


@router.delete("/{book_id}", response_model=Book)
async def delete_book(book_id: int):
    global books
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        return {"error": "Book not found"}
    books = [b for b in books if b["id"] != book_id]
    return book
