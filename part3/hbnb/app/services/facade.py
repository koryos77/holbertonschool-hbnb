from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenities import Amenity
from app.models.places import Place
from app.models.reviews import Review
import uuid

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # User
    def create_user(self, user_data):
        """Create a new user with the provided data."""
        if self.get_user_by_email(user_data['email']):
            raise ValueError('Email already registered')

        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            password=user_data['password']
        )
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by their ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve a user by their email."""
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Retrieve all users from the repository."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update a user's information."""
        user = self.user_repo.get(user_id)
        if not user:
            return None


        if 'email' in user_data and user_data['email'] != user.email:
            existing_user = self.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                raise ValueError('Email already registered')

        if 'password' in user_data:
            user.hash_password(user_data['password'])
        if 'first_name' in user_data:
            user.first_name = user_data['first_name']
        if 'last_name' in user_data:
            user.last_name = user_data['last_name']
        if 'email' in user_data:
            user.email = user_data['email']

        return user

    #Amenity
    def create_amenity(self, amenity_data):
        """Create a new amenity with the provided data."""
        name = amenity_data.get('name')
        if not name:
            raise ValueError("Name is required")
        amenity = Amenity(name=name)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by its ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieve all amenities from the repository."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity's information."""
        amenity = self.get_amenity(amenity_id)
        if amenity and 'name' in amenity_data:
            amenity.name = amenity_data['name']
            amenity.save()
            return amenity
        return None


    #Place
    def create_place(self, place_data):
        """Create a new place with the provided data."""
        required_fields = ['title', 'price', 'latitude', 'longitude', 'owner_id']
        for field in required_fields:
            if field not in place_data or place_data[field] is None:
                raise ValueError(f"{field} is required")

        owner = self.user_repo.get(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found")

        amenity_ids = place_data.get('amenities', [])
        amenities = []
        for amenity_id in amenity_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity {amenity_id} not found")
            amenities.append(amenity)

        try:
            place = Place(
                title=place_data['title'],
                description=place_data.get('description', ''),
                price=place_data['price'],
                latitude=place_data['latitude'],
                longitude=place_data['longitude'],
                owner=owner
            )
            for amenity in amenities:
                place.add_amenity(amenity)
            self.place_repo.add(place)
            return place
        except ValueError as e:
            raise ValueError(str(e))

    def get_place(self, place_id):
        """Retrieve a place by its ID."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieve all places."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update a place's information."""
        place = self.place_repo.get(place_id)
        if not place:
            return None

        try:
            if 'title' in place_data and place_data['title'] is not None:
                place.title = place_data['title']
            if 'description' in place_data:
                place.description = place_data['description']
            if 'price' in place_data and place_data['price'] is not None:
                place.price = place_data['price']
            if 'latitude' in place_data and place_data['latitude'] is not None:
                place.latitude = place_data['latitude']
            if 'longitude' in place_data and place_data['longitude'] is not None:
                place.longitude = place_data['longitude']
            if 'owner_id' in place_data and place_data['owner_id'] is not None:
                owner = self.user_repo.get(place_data['owner_id'])
                if not owner:
                    raise ValueError("Owner not found")
                place.owner = owner
            if 'amenities' in place_data and place_data['amenities'] is not None:
                place.amenities = []
                for amenity_id in place_data['amenities']:
                    amenity = self.amenity_repo.get(amenity_id)
                    if not amenity:
                        raise ValueError(f"Amenity {amenity_id} not found")
                    place.add_amenity(amenity)
            place.save()
            return place
        except ValueError as e:
            raise ValueError(str(e))

    #Reviews
    def create_review(self, review_data):
        """Create a new review with validation."""
        required_fields = ['text', 'rating', 'user_id', 'place_id']
        for field in required_fields:
            if field not in review_data or review_data[field] is None:
                raise ValueError(f"{field} is required")

        user = self.get_user(review_data['user_id'])
        if not user:
            raise ValueError("User not found")

        place = self.get_place(review_data['place_id'])
        if not place:
            raise ValueError("Place not found")

        try:
            review = Review(
                text=review_data['text'],
                rating=review_data['rating'],
                user=user,
                place=place
            )
            self.review_repo.add(review)
            place.reviews.append(review)
            return review
        except ValueError as e:
            raise ValueError(str(e))

    def get_review(self, review_id):
        """Retrieve a review by ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieve all reviews."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Retrieve all reviews for a specific place."""
        place = self.get_place(place_id)
        if not place:
            return None
        return place.reviews

    def update_review(self, review_id, review_data):
        """Update a review's text and rating."""
        review = self.get_review(review_id)
        if not review:
            return None
        if 'text' in review_data:
            review.text = review_data['text']
        if 'rating' in review_data:
            review.rating = review_data['rating']
        review.save()
        return review

    def delete_review(self, review_id):
        """Delete a review by ID."""
        review = self.get_review(review_id)
        if review:
            review.place.reviews.remove(review)
            self.review_repo.delete(review_id)
            return True
        return False

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_place(self, place_id):
        return self.place_repo.get(place_id)
