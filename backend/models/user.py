from db import db
from sqlalchemy.dialects.postgresql import ARRAY

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    mobile_number = db.Column(db.String(255))
    status = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    roles = db.Column(ARRAY(db.String))

    def __init__(self, full_name, email, password, roles):
        self.full_name = full_name
        self.email = email
        self.password = password
        self.status = 'pending_approval'
        self.roles = roles

    def get_json(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'mobile_number': self.mobile_number,
            'created_at': str(self.created_at) if self.created_at else None,
            'updated_at': str(self.updated_at) if self.updated_at else None,
            'status': self.status,
            'roles': self.roles
        }