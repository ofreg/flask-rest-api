from flask import request, jsonify
from flask_restful import Resource
from flasgger import swag_from

from api.models import get_all_books, get_book_by_id, add_book, delete_book_by_id
from api.schemas import book_model

class Book(Resource):
    @swag_from({
        'responses': {
            200: {
                'description': 'Отримати список книг',
                'examples': {
                    'application/json': [
                        {'id': 1, 'title': 'Book 1', 'author': 'Author 1'}
                    ]
                }
            }
        }
    })
    def get(self):
        return jsonify(get_all_books())

    @swag_from({
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': book_model
            }
        ],
        'responses': {
            201: {'description': 'Книга додана'}
        }
    })
    def post(self):
        data = request.get_json()
        book = add_book(data['title'], data['author'])
        return book, 201

class BookById(Resource):
    @swag_from({
        'parameters': [
            {
                'name': 'book_id',
                'in': 'path',
                'type': 'integer',
                'required': True
            }
        ],
        'responses': {
            200: {'description': 'Книга знайдена'},
            404: {'description': 'Книга не знайдена'}
        }
    })
    def get(self, book_id):
        book = get_book_by_id(book_id)
        if book:
            return book
        return {'message': 'Book not found'}, 404

    @swag_from({
        'parameters': [
            {
                'name': 'book_id',
                'in': 'path',
                'type': 'integer',
                'required': True
            }
        ],
        'responses': {
            200: {'description': 'Книга видалена'},
            404: {'description': 'Книга не знайдена'}
        }
    })
    def delete(self, book_id):
        if delete_book_by_id(book_id):
            return {'message': 'Book deleted'}, 200
        return {'message': 'Book not found'}, 404
