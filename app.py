from flask import Flask
from flasgger import Swagger
from api import api_bp

def create_app():
    app = Flask(__name__)
    Swagger(app)

    
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
