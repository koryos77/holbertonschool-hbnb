# HBnB Project

This project implements a Flask-based API for the HBnB application.

## Directory Structure

- `app/`: Core application code
  - `api/`: API endpoints (v1)
  - `models/`: Business logic classes
  - `services/`: Facade pattern implementation
  - `persistence/`: In-memory repository (to be replaced with database)
- `run.py`: Entry point for running the Flask application
- `config.py`: Application configuration
- `requirements.txt`: Python package dependencies

## Setup and Running

1. Install dependencies
2. Run the application


## Business Logic Layer

The Business Logic layer defines the core entities of the HBnB application:

- **User**: Represents a user with attributes `first_name`, `last_name`, `email`, and `is_admin`.
- **Place**: Represents a rental property with attributes `title`, `description`, `price`, `latitude`, `longitude`, and `owner`.
- **Review**: Represents a review with attributes `text`, `rating`, `place`, and `user`.
- **Amenity**: Represents a feature with a `name`.

All entities inherit from `BaseModel`, which provides `id` (UUID), `created_at`, and `updated_at`.

### Relationships
- A `User` can own multiple `Place` instances.
- A `Place` can have multiple `Review` and `Amenity` instances.
- A `Review` is linked to one `Place` and one `User`.

### Example Usage
```python
# Create a user
user = User(first_name="John", last_name="Doe", email="john.doe@example.com")

# Create a place
place = Place(title="Cozy Apartment", description="Nice stay", price=100, latitude=37.7749, longitude=-122.4194, owner=user)

# Add an amenity
amenity = Amenity(name="Wi-Fi")
place.add_amenity(amenity)

# Add a review
review = Review(text="Great stay!", rating=5, place=place, user=user)
place.add_review(review)
```

### Example with cURL
**create new user**

curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"
}'

**Retrieve user with id**
curl -X GET http://localhost:5000/api/v1/users/<user_id>

**Invalid data for user**
curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{
    "first_name": "",
    "last_name": "",
    "email": "invalid-email"
}'

**Retrieve all users**
curl -X GET http://localhost:5000/api/v1/users/


**User not found**
curl -X PUT http://localhost:5000/api/v1/users/non-existent-id \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Jane"
}'

**Create new amenity**
curl -X POST http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi"
}'

**Retrieve all amenities**
curl -X GET http://localhost:5000/api/v1/amenities/

**Create new Place**
curl -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Cozy Apartment",
    "description": "A nice place to stay",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "amenities": ["4fa85f64-5717-4562-b3fc-2c963f66afa6", "5fa85f64-5717-4562-b3fc-2c963f66afa6"]
}'

**Retrieve all places**
curl -X GET http://localhost:5000/api/v1/places/

**Create review**
curl -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Great place to stay!", "rating": 5, "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "place_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6"
}'

**Delete review**
curl -X DELETE http://localhost:5000/api/v1/reviews/<review_id>




## Authors
- Kevin Rouget
- Keita Mouhamed
