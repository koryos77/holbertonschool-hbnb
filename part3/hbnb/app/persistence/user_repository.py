from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)
    
    def get_by_email(self, email):
        """Get a user by email"""
        return self.get_by_attribute('email', email)
    
    def create_user(self, user_data):
        """Create a new user"""
        if self.get_by_email(user_data.get('email')):
            raise ValueError('Email already registered')
        
        user = User(**user_data)
        self.add(user)
        return user
    
    def update_user(self, user_id, user_data):
        """Update a user"""
        user = self.get(user_id)
        if not user:
            return None
            
        if 'email' in user_data and user_data['email'] != user.email:
            existing_user = self.get_by_email(user_data['email'])
            if existing_user:
                raise ValueError('Email already registered')

        user.update(user_data)
        return user
