from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Place not found')
    @jwt_required
    def post(self):
        """Register a new review"""
        try:
            current_user = get_jwt_identity()
            review_data = api.payload.copy()
            place_id = review_data.get('place_id')

            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404
            
            if str(place.owner_id) == current_user:
                return {'error': 'Cant review own place'}, 400
            
            exist_review = facade.get_reviews_by_place(place_id)
            if any(str(review.user_id) == current_user for review in exist_review):
                return {'error': 'Can not review a place multiple times'}, 400
            
            review_data['user_id'] = current_user
            new_review = facade.create_review(review_data)
            return new_review.to_dict(), 201
        except Exception as e:
            return {'error': 'Failed to create a review'}, 500

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        return [review.to_dict() for review in facade.get_all_reviews()], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required
    def put(self, review_id):
        """Update a review's information"""
        try:
            current_user = get_jwt_identity()
            review = facade.get_review(review_id)
            if not review:
                return {'error': 'Review not found'}, 404
            
            if str(review.user_id) != current_user:
                return {'error': 'Unauthorized action'}, 403
            
            review_data = api.payload
            facade.update_review(review_id, review_data)
            return {'message': 'Review updated successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required
    def delete(self, review_id):
        """Delete a review"""
        try:
            current_user = get_jwt_identity()
            review = facade.get_review(review_id)
            if not review:
                return {'error': 'Review not found'}, 404
            
            if str(review.user_id) != current_user:
                return {'error': 'Unauthorized action'}, 403
            
            facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
