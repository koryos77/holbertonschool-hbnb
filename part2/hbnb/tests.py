from app.models.user import User
from app.models.places import Place
from app.models.reviews import Review
from app.models.amenities import Amenity

def test_user_creation():
    """Test user creation and validation"""
    try:
        user = User(first_name="John", last_name="Jones", email="john.jones@example.com")
        assert user.first_name == "John"
        assert user.last_name == "Jones"
        assert user.email == "john.jones@example.com"
        assert user.is_admin is False
        print("User creation test passed successfully!")
    except Exception as e:
        print(f"User creation test failed: {str(e)}")

def test_place_creation():
    """Test place creation"""
    try:
        owner = User(first_name="Randy", last_name="Marsch", email="randy.marsch@example.com")
        place = Place(
            title="Nice place in South park",
            description="A great place to stay",
            price=170,
            latitude=56.7649,
            longitude=118.2594,
            owner=owner
        )

        assert place.title == "Nice place in South park"
        assert place.price == 170.0
        assert place.owner == owner
        assert place in owner.places
        print("Place creation and test passed successfully!")
    except Exception as e:
        print(f"Place creation test failed: {str(e)}")

def test_review_creation():
    """Test review creation"""
    try:
        user = User(first_name="Eric", last_name="Cartman", email="eric.cartman@example.com")
        owner = User(first_name="Kyle", last_name="Broflovski", email="kyle.b@example.com")
        place = Place(
            title="House in the mountains",
            description="Amazing place in the mountains",
            price=150,
            latitude=45.7857,
            longitude=115.2058,
            owner=owner
        )
        review = Review(text="Horrible place !", rating=1, place=place, user=user)

        assert review.text == "Horrible Place !"
        assert review.rating == 1
        assert review in place.reviews
        print("Review creation test passed successfully!")
    except Exception as e:
        print(f"Review creation test failed: {str(e)}")

def test_amenity_creation():
    """Test amenity creation"""
    try:
        owner = User(first_name="Homer", last_name="Simpson", email="homer.simpson@example.com")
        place = Place(
            title="House in Springfield",
            description="Nice House in Springfield just near the power plant !",
            price=90,
            latitude=44.1475,
            longitude=95.8482,
            owner=owner
        )
        swimming_pool = Amenity(name="Swimming pool")
        wifi = Amenity(name="Wi-Fi")

        place.add_amenity(swimming_pool)
        place.add_amenity(wifi)

        assert wifi in place.amenities
        assert swimming_pool in place.amenities
        assert len(place.amenities) == 2
        print("Amenity creation test passed successfully!")
    except Exception as e:
        print(f"Amenity creation test failed: {str(e)}")

def test_validation():
    """Test input validation"""
    try:
        try:
            User(first_name="Abraham", last_name="Simpson", email="iiikljaf")
            print("Invalid email test failed: Invalid email accepted")
        except ValueError:
            print("Invalid email validation test passed successfully!")

        try:
            user = User(first_name="John", last_name="Kennedy", email="johnkennedy@example.com")
            owner = User(first_name="Gengis", last_name="Khan", email="gk@example.com")
            place = Place(title="Place", description="description", price=200, latitude=44.1475, longitude=115.2058, owner=owner)
            Review(text="Test review", rating=10, place=place, user=user)
            print("Invalid rating test failed: Invalid rating was accepted")
        except ValueError:
            print("Invalid rating validation test passed!")

        try:
            owner = User(first_name="John", last_name="Snow", email="js@example.com")
            Place(title="Place", description="description", price=-10, latitude=44.1476, longitude=115.2058, owner=owner)
            print("Invalid price test failed: Wrong price accepted")
        except ValueError:
            print("Invalid price validation test passed successfully!")


    except Exception as e:
        print(f"Validation tests failed: {str(e)}")

if __name__ == "__main__":
    test_user_creation()
    test_place_creation()
    test_review_creation()
    test_amenity_creation()
    test_validation()
