from fastapi import FastAPI
from api.views import books_router
from api.auth import auth_router

app = FastAPI()

app.include_router(auth_router, prefix="/api/v1/auth")

app.include_router(books_router, prefix="/api/v1/books")
