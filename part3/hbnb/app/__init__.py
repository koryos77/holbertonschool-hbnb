from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_api
from app.api.v1.protected import api as protected_api
from app.extensions import bcrypt, jwt, db

def create_app(config_class="config.DevelopmentConfig"):
    # Function to initialize and configure the Flask app.
    app = Flask(__name__)
    app.config.from_object(config_class)
    # Create the API instance, with version and description.
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    # Initialize the app with bcrypt, jwt, and db extensions
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Adding API namespaces, which map to the different resources in your app.
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_api, path='/api/v1/auth')
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
