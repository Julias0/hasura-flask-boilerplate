from datetime import datetime
import enum
import json
from requests import Response

class GeneralObject(object):
    def __init__(self, object_as_dict):
        self.__dict__ = object_as_dict

    def __getattr__(self, item):
        return None
 
    def __repr__(self):
        return self.__dict__.__str__()

def deserialize(dictionary):
    if not isinstance(dictionary, dict):
        return dictionary
    
    for key, value in dictionary.items():
        if isinstance(value, dict):
            deserialized_value = deserialize(value)
            dictionary[key] = deserialized_value
        elif isinstance(value, list):
            for index, item in enumerate(value):
                deserialized_item = deserialize(item)
                value[index] = deserialized_item
            dictionary[key] = value
    deserialized_object = GeneralObject(dictionary)
    return deserialized_object

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Response):
            try:
                return obj.json()
            except:
                return {}
        elif isinstance(obj, datetime):
            return obj.isoformat() + "Z"
        elif isinstance(obj, enum.Enum):
            return obj.value
        elif isinstance(obj, GeneralObject):
            return obj.__dict__
        elif hasattr(obj, '__class__'):
            if hasattr(obj, 'serialize'):
                return obj.serialize()
            else:
                return None
        elif isinstance(obj, Exception):
            return {
                "error": obj.__class__.__name__,
                "args": obj.args,
            }
        return json.JSONEncoder.default(self, obj)

def serialize(instance, **kwargs):
    return json.dumps(instance, cls=ComplexEncoder, **kwargs)