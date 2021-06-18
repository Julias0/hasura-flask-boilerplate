from flask_restful import Resource, reqparse, abort
from state_machines.user import UserStateMachine
from bcrypt import hashpw, gensalt
from utils.helpers import assert_true

class SignUpResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True, help='email is a required field')
        parser.add_argument('full_name', required=True, help='full_name is a required field')
        parser.add_argument('role', required=True, help='role is a required field')
        parser.add_argument('password', required=True, help='password is a required field')

        args = parser.parse_args()

        assert_true(args['role'] in ['general', 'owner', 'admin'],message='incorrect role passed',status_code=400)

        existing_user = UserStateMachine.get_user_by_email(args['email'])

        if existing_user is not None:
            return {
                'message': 'user already exists'
            }, 400

        hashed_pwd = hashpw(args['password'].encode('utf8'), gensalt())
        user = UserStateMachine.register_user(args['email'], args['full_name'], hashed_pwd.decode('utf8'), args['role'])

        return {
            'status': 'success',
            'user': user.get_json()
        }