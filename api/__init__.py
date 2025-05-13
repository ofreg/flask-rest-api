from flask import Blueprint
from flask_restful import Api

from api.views import Book, BookById


api_bp = Blueprint('api', __name__)
api = Api(api_bp)


api.add_resource(Book, '/books')
api.add_resource(BookById, '/books/<int:book_id>')
