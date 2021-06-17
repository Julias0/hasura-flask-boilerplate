from models.user import UserModel
from db import db

class UserStateMachine:
    @staticmethod
    def get_user_by_email(email):
       user = db.session.query(UserModel).filter_by(email=email).first()
       return user
    
    @staticmethod
    def register_user(email, full_name, hashed_password, role):
        user = UserModel(full_name, email, hashed_password, ['general'] if role == 'general' else ['general', role])
        db.session.add(user)
        db.session.commit()

        return user