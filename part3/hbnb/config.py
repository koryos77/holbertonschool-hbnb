import os

class Config:
    # SECRET_KEY is used for various cryptographic operations, like session management
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False

class DevelopmentConfig(Config):
    # Overriding DEBUG to True for the development environment, 
    # enabling features like debugging tools and detailed error messages.
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hbnb_database.db'
    SQLALCHEMY_TRACK_MODIFICATION = False

# Dictionary mapping environment names to the configuration classes
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
