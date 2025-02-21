from flask import Flask
from .views import books_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(books_bp, url_prefix="/api/v1/books")
    return app
