from app.models.user import User
from sqlalchemy import func
from app.extensions import db
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)
    
    def get_by_attribute(self, attribute, value):
        if attribute == '_email':
            return self.model.query.filter(func.lower(getattr(self.model, attribute)) == value.lower()).first()
        return super().get_by_attribute(attribute, value)

    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()

    def get_user_by_first_name(self, first_name):
        return self.model.query.filter_by(first_name=first_name).first()

    def get_user_by_last_name(self, last_name):
        return self.model.query.filter_by(last_name=last_name).first()

    def get_users_by_role(self, role):
        return User.query.filter_by(role=role).all()
    
    def get_all_users(self):
        return self.model.query.all()
    
    def deactivate_user(self, user_id):
        user = self.get_by_attribute(user_id)
        if user:
            user.is_active = False
            db.session.commit()
            return True
        return False
    
    def authenticate_user(self, email, password):
        user = self.get_user_by_email(email)
        if user and user.verify_password(password):
            return user
        return None
