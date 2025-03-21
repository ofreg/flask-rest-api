from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    
    db.init_app(app)
    
    
    from . import models

    
    from .views import books_bp

    
    app.register_blueprint(books_bp, url_prefix="/api/v1/books")

    return app
