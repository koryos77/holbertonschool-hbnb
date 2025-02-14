```mermaid

classDiagram
    class BaseModel {
        +Id
        +DateTime created_at
        +DateTime updated_at
        +save()
        +to_dict()
    }
    
    class User {
        -String First_name
        -String Last_name
        +String Pseudo
        +String Email
        #String Password
        +Boolean Is_admin
        +Boolean Is_registered
        +Register()
        +Log_in()
        +Update_profile()
    }
    
    class Place {
        +String Title
        +String Description
        +Float Price
        +Address
        +User Owner
        +List Amenities
        +Create_place()
        +Update_place()
        +Delete_place()
        +Rent_place()
        +Add_amenity()
        +Remove_amenity()
    }
    
    class Review {
        +User Author
        +Place Place
        +Int Rating
        +String Comment
        +Create_review()
        +Update_review()
        +Delete_review()
    }

    class Amenity {
        +String Name
        +String Description
        +Create_amenity()
        +Update_amenity()
        +Delete_amenity()
    }

    BaseModel <|-- User
    BaseModel <|-- Place
    BaseModel <|-- Review
    BaseModel <|-- Amenity
    Amenity --|> Place
    Review --|> Place

```


## BaseModel
The BaseModel class is used as a base class to define data models.

## User
The User class represent an user of the HBnB.
It has attributes that defines his ID.
It has methods to check if User is registered, if he wants to log in or sign in, or updating the profile.

## Place
The Place class represents a place to rent.
It has attributes that describe the place.
It has methods to create, update a place, add amenities or remove amenities, and to rent it.

## Review
The Review class represents a review about a place.
It has attributes for the authors, the rating and to comment.
It has methods to create, update or delete a comment.

## Amenity
The Amenity class represents the amenities of a place.
It has attributes for name and description of the amenities.
It has methods to create, update or delete an amenity.