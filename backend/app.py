from flask import Flask, jsonify
from flask_restful import Api, abort
from flask_migrate import Migrate
from flask_cors import CORS
import os
from db import db
from models import user
from utils.helpers import InvalidUsage

from resources.sign_in import SignInResource
from resources.sign_up import SignUpResource

class CustomApi(Api):
    def handle_error(self, err):
        """It helps preventing writing unnecessary
        try/except block though out the application
        """
        print(err) # log every exception raised in the application
        # Handle HTTPExceptions
        if isinstance(err, InvalidUsage):
            return jsonify(err.to_dict()), err.status_code
        # If msg attribute is not set,
        # consider it as Python core exception and
        # hide sensitive error info from end user
        if not getattr(err, 'message', None):
            return jsonify({
                'message': 'Server has encountered some error'
                }), 500
        # Handle application specific custom exceptions
        return jsonify(**err.kwargs), err.http_status_code

api = CustomApi()
migrate = Migrate()
cors = CORS()

api.add_resource(SignInResource, '/sign_in')
api.add_resource(SignUpResource, '/sign_up')

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('FLASK_DATABASE_URL')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['TRAP_HTTP_EXCEPTIONS']=True

    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    @app.route('/')
    def helloWorld():
        return """
            Thank you so much for visiting. This is the api 
        """

    @app.after_request
    def add_header(response):
        response.headers['Content-Type'] = 'application/json'
        return response

    return app