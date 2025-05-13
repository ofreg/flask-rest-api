# Проста модель (можна підключити БД)
books = []

def get_all_books():
    return books

def get_book_by_id(book_id):
    return next((book for book in books if book['id'] == book_id), None)

def add_book(title, author):
    book_id = len(books) + 1
    book = {
        'id': book_id,
        'title': title,
        'author': author
    }
    books.append(book)
    return book
