from . import serializers

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def assert_true(condition, message='Forbidden', status_code=403):
    if condition is False: 
        raise InvalidUsage(message, status_code=status_code)

def assert_found(instance, message='Not Found', status_code=404):
    if instance is None:
        raise InvalidUsage(message, status_code=status_code)

def assert_valid(condition, message='Bad Request', status_code=400):
    if condition is False: 
        raise InvalidUsage(message, status_code=status_code)

def assert_good(value, message='Internal Server Error'):
    assert_true(value, status_code=500, message=message)

def assert_found(instance, message='Not found'):
    if instance is None:
        raise InvalidUsage(message=message, status_code=404)

def assert_auth(condition, message='Unauthorized', status_code=401):
    if condition is False:
        raise InvalidUsage(message, status_code=status_code)

def respond(object_instance):
    result = serializers.serialize(object_instance)
    return result, 200