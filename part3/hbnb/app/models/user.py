from app.models.base_model import BaseModel
import re
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hash_password(password)
        self.is_admin = is_admin


    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str) or not value or len(value) > 50:
            raise ValueError("First name must be a non-empty string <= 50 characters")
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str) or not value or len(value) > 50:
            raise ValueError("Last name must be a non-empty string <= 50 characters")
        self._last_name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not isinstance(value, str) or not self.validate_email(value):
            raise ValueError("Invalid email format")
        self._email = value

    @staticmethod
    def validate_email(email):
        """Validate email format using a regular expression"""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    @property
    def password(self):
        return None

    @password.setter
    def hash_password(self, password):
        """Hashes the password before storing it."""
        self._password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        if self._password is None:
            return False
        return bcrypt.check_password_hash(self._password, password)

    def to_dict(self):
        """Convert user in dict without the password"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        }
