import jwt
import os
from flask import request
import datetime


class AuthUtils:
    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            return jwt.decode(auth_token, os.getenv('SECRET_KEY'), algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise ValueError('Signature expired. Please log in again.')
        except jwt.InvalidTokenError:
            raise ValueError('Invalid token. Please log in again.')

    @staticmethod
    def get_token(request):
        auth_header = request.headers.get('Authorization')
        auth_token = None
        if auth_header:
            auth_token = auth_header.split(' ')[1]

        if auth_token is not None:
            return AuthUtils.decode_auth_token(auth_token)
        else:
            raise ValueError('Token should be present')

    @staticmethod
    def jwt_required(func):
        def inner(*args, **kwargs):
            try:
                token = AuthUtils.get_token(request)
            except ValueError:
                return {
                    'message': 'unauthenticated'
                }, 401

            return func(*args, **kwargs, token=token)
        return inner

    @staticmethod
    def intersection(lst1, lst2):
        return list(set(lst1) & set(lst2))

    @staticmethod
    def check_roles_required(required_roles):
        def outer(func):
            def inner(*args, **kwargs):
                try:
                    token = AuthUtils.get_token(request)
                    current_user_roles = token['user']['roles']
                    if len(AuthUtils.intersection(required_roles, current_user_roles)) > 0:
                        return func(*args, **kwargs)
                    else:
                        return {
                            'message': 'permissions not valid'
                        }, 401
                except ValueError:
                    raise ValueError
                    return {
                        'message': 'unauthenticated'
                    }, 401
            return inner
        return outer

    @staticmethod
    def get_access_token(user):
        days=30
        details = {
            'user': user.get_json(),
            'https://hasura.io/jwt/claims': {
                'x-hasura-allowed-roles': user.roles,
                'x-hasura-default-role': 'general',
                'x-hasura-user-id': str(user.id)
            },
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=days)
        }

        access_token = jwt.encode(details, os.getenv('SECRET_KEY'), algorithm='HS256')
        return access_token
