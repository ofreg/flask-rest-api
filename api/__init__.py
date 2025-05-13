from flask import Blueprint
from flask_restful import Api

from api.views import Book, BookById

# Ініціалізуємо Blueprint та API
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Реєстрація ресурсів
api.add_resource(Book, '/books')
api.add_resource(BookById, '/books/<int:book_id>')
