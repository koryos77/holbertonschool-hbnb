-- Testing CRUD (Create, Read, Update and Delete) on HBnB database

--CREATE

INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    'idTestUser',
    'John',
    'Doe',
    'john_doe@test.com',
    '',
    FALSE
);

INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
VALUES (
    'idTestPlace',
    'Place Test',
    'A really nice testing place to test many things',
    '500.00',
    '41.4598',
    '125.3695',
    'Owner TestId'
);

INSERT INTO reviews (id, text, rating, user_id, place_id)
VALUES (
    'idReviewsTest',
    'Review Test',
    5,
    'userIdTest',
    'placeIdTest'
);

INSERT INTO amenities (id, name)
VALUES (
    'idAmenitiesTest',
    'Amenity Test'
);

-- READ

-- UPDATE

-- DELETE
