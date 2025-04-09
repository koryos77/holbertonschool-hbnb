import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False
    
    ADMIN_EMAIL = 'admin@hbnb.io'
    ADMIN_PASSWORD = 'admin1234'
    ADMIN_FIRST_NAME = 'Admin'
    ADMIN_LAST_NAME = 'HBnB'
    ADMIN_ID = '36c9050e-ddd3-4c3b-9731-9f487208bbc1'
    
    INITIAL_AMENITIES = ['WiFi', 'Swimming Pool', 'Air Conditioning']

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_ORIGINS = ['http://localhost:5500', 'http://127.0.0.1:5500']
    CORS_SUPPORTS_CREDENTIALS = True
    JWT_UNAUTHORIZED_RESPONSE = {'message': 'Missing or invalid token'}, 401

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig,
}