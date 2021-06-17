from flask_restful import Resource, reqparse
from state_machines.user import UserStateMachine
import bcrypt
import jwt
import os
from db import db
from utils.auth import AuthUtils


class SignInResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True, help='email is a required field')
        parser.add_argument('password', required=True, help='password is a required field')

        args = parser.parse_args()

        existing_user = UserStateMachine.get_user_by_email(args['email'])

        if existing_user is None:
            return {
                       'message': 'User does not exist'
                   }, 400

        if bcrypt.checkpw(args['password'].encode('utf8'), str(existing_user.password).encode('utf8')):
            access_token = AuthUtils.get_access_token(existing_user)
            return {
                'access_token': access_token
            }
        else:
            return {
                    'message': 'incorrect password',
                }, 400