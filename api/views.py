from .schemas import book_schema, book_list_schema
from flask import Blueprint, request, jsonify, Response
from marshmallow import ValidationError
import json
from .models import books
books_bp = Blueprint("books", __name__)


@books_bp.route("/", methods=["GET"])
def get_books():
    return Response(
        json.dumps(books, ensure_ascii=False, indent=4), 
        mimetype="application/json"
    )

@books_bp.route("/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    return Response(
        json.dumps(book_schema.dump(book), ensure_ascii=False),  
        mimetype="application/json"
    )

@books_bp.route("/", methods=["POST"])
def add_book():
    try:
        new_book = book_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    
    new_id = max([book["id"] for book in books], default=0) + 1
    new_book["id"] = new_id 

    books.append(new_book)
    return Response(
        json.dumps(book_schema.dump(new_book), ensure_ascii=False),  
        mimetype="application/json"
    )

@books_bp.route("/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    global books
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        return jsonify({"error": "Book not found"}), 404

    books = [book for book in books if book["id"] != book_id]
    return jsonify({"message": "Book deleted"}), 200
