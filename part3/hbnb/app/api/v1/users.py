from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from flask import request

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'is_admin': fields.Boolean(required=False, description='Admin status')
})

# Define the admin model for input validation and documentation
admin_user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'is_admin': fields.Boolean(required=True, description='Admin status')
})
admin_amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'is_admin': fields.Boolean(required=True, description='Admin status')
})
admin_place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's"),
    'is_admin': fields.Boolean(required=True, description='Admin status')
})
admin_review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place'),
    'is_admin': fields.Boolean(required=True, description='Admin status')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400
        
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of users"""
        users = facade.get_users()
        return [user.to_dict() for user in users], 200
    
@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @api.expect(user_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, user_id):
        try:
            current_user = get_jwt_identity()

            if str(user_id) != current_user:
                return {'error': 'Unauthorized action'}, 403
            
            user = facade.get_user(user_id)
            if not user:
                return {'error': 'User not found'}, 404
            user_data = api.payload
            if 'email' in user_data or 'password' in user_data:
                return {'error': 'Invalid input data'}, 400
            
            updated_user = facade.update_user(user_id, user_data)
            return updated_user.to_dict(), 200
        
        except ValueError as e:
            return {'error': str(e)}, 400

@api.route('/users/')
class AdminUserCreate(Resource):
    @api.expect(admin_user_model)
    @api.response(201, "User created successfully")
    @api.response(400, "Email already registered")
    @api.response(403, "Admin privileges required")
    @jwt_required()
    def post(self):
        """Admin - Register a new user"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = request.json
        email = user_data.get('email')

        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except Exception as e:
            return {'error': f'Failed to create user: str(e)'}, 400

@api.route('/users/<user_id>')
class AdminUserModify(Resource):
    @api.expect(admin_user_model)
    @api.response(200, "User updated successfully")
    @api.response(400, "Invalid input")
    @api.response(403, "Admin privileges required")
    @api.response(404, "User not found")
    @jwt_required()
    def put(self, user_id):
        """Admin - Modify user information"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email')
        existing_user = facade.get_user(user_id)

        if not existing_user:
            return {'error': 'User not found'}, 404
        if email:
            if email and email != facade.get_user_by_email(email):
                return {'error': 'Email is already in use'}, 400

        try:
            updated_user = facade.update_user(user_id, data)
            return updated_user.to_dict(), 200
        except Exception as e:
            return {'error': f'Update failed: {str(e)}'}, 400

@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @api.expect(admin_amenity_model)
    @api.response(201, "Amenity created successfully")
    @api.response(400, "Invalid input")
    @api.response(403, "Admin privileges required")
    @jwt_required()
    def post(self):
        """Admin - Register new amenity"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        amenity_data = request.json
        if not amenity_data.get('name'):
            return {'error': 'Amenity name is required'}
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return new_amenity.to_dict(), 201
        except Exception as e:
            return {'error': f'Failed to create amenity: {str(e)}'}, 400

@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @api.expect(admin_amenity_model)
    @api.response(200, "Amenity updated successfully")
    @api.response(400, "Invalid input")
    @api.response(403, "Admin privileges required")
    @api.response(404, "Amenity not found")
    @jwt_required()
    def put(self, amenity_id):
        """Admin - Modify amenity details"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        amenity_data = request.json
        existing_amenity = facade.get_amenity(amenity_id)
        if not existing_amenity:
            return {'error': 'Amenity not found'}, 404
        if not amenity_data:
            return {'error': 'No update data provided'}, 400
        
        try:
            update_amenity = facade.update_amenity(amenity_id, amenity_data)
            return update_amenity.to_dict(), 200
        except Exception as e:
            return {'error': f'Failed to update amenity: {str(e)}'}, 400

@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @api.expect(admin_place_model)
    @api.response(204, "Place updated successfully")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Place not found")
    @jwt_required
    def put(self, place_id):
        """Admin - Modify place informations"""
        current_user = get_jwt_identity
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')
        
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403
        
        try:
            update_data = request.json
            updated_place = facade.update_place(place_id, update_data)
            return updated_place.to_dict(), 200
        except Exception as e:
            return {'error': f'Failed to update place: {str(e)}'}, 400
    
    @api.response(200, "Place deleted successfully")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Place not found")
    def delete(self, place_id):
        """Admin - Delete place"""
        current_user = get_jwt_identity
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')
        
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403
        
        try:
            facade.delete_place(place_id)
            return '', 204
        except Exception as e:
            return {'error': f'Failed to delete place: {str(e)}'}, 500

@api.route('/reviews/<review_id>')
class AdminReviewModify(Resource):
    @api.expect(admin_review_model)
    @api.response(204, "Review updated successfully")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Review not found")
    @jwt_required
    def put(self, review_id):
        """Admin - Modify review informations"""
        current_user = get_jwt_identity
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')
        
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        if not is_admin and review.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403
        
        try:
            update_data = request.json
            updated_review = facade.update_review(review_id, update_data)
            return updated_review.to_dict(), 200
        except Exception as e:
            return {'error': f'Failed to update review: {str(e)}'}, 400
    
    @api.response(200, "Review deleted successfully")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Review not found")
    def delete(self, review_id):
        """Admin - Delete review"""
        current_user = get_jwt_identity
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')
        
        review = facade.get_place(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        if not is_admin and review.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403
        
        try:
            facade.delete_review(review_id)
            return '', 204
        except Exception as e:
            return {'error': f'Failed to delete review: {str(e)}'}, 500
