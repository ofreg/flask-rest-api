from flask import Blueprint, request, jsonify
from . import db
from .models import Book
from .schemas import BookSchema

books_bp = Blueprint('books', __name__)


@books_bp.route("/", methods=["POST"])
def create_book():
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")

    if not title:
        return jsonify({"message": "Title is required"}), 400

    book = Book(title=title, description=description)
    db.session.add(book)
    db.session.commit()

    book_schema = BookSchema()
    return jsonify(book_schema.dump(book)), 201

@books_bp.route("/<int:book_id>", methods=["GET"])
def get_book(book_id):
   
    book = Book.query.get(book_id)
    
    if not book:
        return jsonify({"message": "Book not found"}), 404
    
    book_schema = BookSchema()
    return jsonify(book_schema.dump(book))



@books_bp.route("/", methods=["GET"])
def get_books():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    
    books = Book.query.paginate(page=page, per_page=per_page, error_out=False)
    
    book_schema = BookSchema(many=True)

    return jsonify({
        "books": book_schema.dump(books.items),
        "total": books.total,
        "page": books.page,
        "per_page": books.per_page
    })




@books_bp.route("/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book=Book.query.get(book_id)
    
    if not book:
        return jsonify({"message": "Book not found"}), 404
    
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully"}), 200

