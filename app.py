from fastapi import FastAPI
from api.views import router
from api.views import router as books_router

app = FastAPI()

app.include_router(books_router, prefix="/api/v1/books")
