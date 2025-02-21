from .schemas import book_schema, book_list_schema
from flask import Blueprint, request, jsonify, Response
from marshmallow import ValidationError
import json
 

books_bp = Blueprint("books", __name__)

books = []


@books_bp.route("/books", methods=["GET"])
def get_books():
    return Response(
        json.dumps(books, ensure_ascii=False), 
        mimetype="application/json"
    )

@books_bp.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book_schema.dump(book)), 200


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


@books_bp.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    global books
    books = [book for book in books if book["id"] != book_id]
    return jsonify({"message": "Book deleted"}), 200
