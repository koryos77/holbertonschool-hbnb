from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('auth', description='Authentication operations')

login_model = api.model('login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.response(401, 'Invalid credentials')
    @api.resources(200, 'Login successful')
    def post(self):
        """Authenticates user and return a JWT token"""
        credentials = api.payload

        admin = facade.authenticate_user(credentials['email'], credentials['password'])

        if not admin:
            return {'error': 'Invalid credentials'}, 401
        return {'access_token': admin}

api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        current_user = get_jwt_identity()
        return {'message': f'Hello, user {current_user["id"]}'}, 200
