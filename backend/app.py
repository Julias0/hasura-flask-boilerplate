from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_cors import CORS
import os
from db import db
from models import user

from resources.sign_in import SignInResource
from resources.sign_up import SignUpResource

api = Api()
migrate = Migrate()
cors = CORS()

api.add_resource(SignInResource, '/sign_in')
api.add_resource(SignUpResource, '/sign_up')

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('FLASK_DATABASE_URL')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    @app.route('/')
    def helloWorld():
        return """
            Thank you so much for visiting. This is the api - visiting klaar.xyz for the web app.
        """

    return app