from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields, ValidationError

books_bp = Blueprint("books", __name__)


books = []


class BookSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    year = fields.Int(required=True)

book_schema = BookSchema()
book_list_schema = BookSchema(many=True)

# 1. Отримання всіх книг
@books_bp.route("/books", methods=["GET"])
def get_books():
    return jsonify(book_list_schema.dump(books))

# 2. Отримання книги за ID
@books_bp.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book_schema.dump(book))

# 3. Додавання книги
@books_bp.route("/books", methods=["POST"])
def add_book():
    try:
        new_book = book_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    if any(book["id"] == new_book["id"] for book in books):
        return jsonify({"error": "Book with this ID already exists"}), 400

    books.append(new_book)
    return jsonify(book_schema.dump(new_book)), 201

# 4. Видалення книги
@books_bp.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    global books
    books = [book for book in books if book["id"] != book_id]
    return jsonify({"message": "Book deleted"})
