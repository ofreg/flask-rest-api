from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from .models import books
from .schemas import Book
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from .rate_limiter import rate_limit

SECRET_KEY = "secret"
ALGORITHM = "HS256"

books_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def verify_token(token: str = Depends(oauth2_scheme)) -> str | None:
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None

@books_router.get("/", response_model=List[Book])
async def get_books(request: Request, username: str | None = Depends(verify_token)):
    await rate_limit(request, username)
    return books

@books_router.get("/{book_id}", response_model=Book)
async def get_book(book_id: int, request: Request, username: str | None = Depends(verify_token)):
    await rate_limit(request, username)
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@books_router.post("/", response_model=Book)
async def add_book(book: Book, request: Request, username: str | None = Depends(verify_token)):
    await rate_limit(request, username)
    new_book = book.dict()
    new_book["id"] = len(books) + 1
    books.append(new_book)
    return new_book

@books_router.delete("/{book_id}", response_model=Book)
async def delete_book(book_id: int, request: Request, username: str | None = Depends(verify_token)):
    await rate_limit(request, username)
    global books
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    books = [b for b in books if b["id"] != book_id]
    return book
