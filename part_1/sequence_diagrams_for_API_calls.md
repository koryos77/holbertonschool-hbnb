# User Registration

```mermaid
sequenceDiagram
    participant Client
    participant API as API Gateway
    participant UserService
    participant UserLogic
    participant UserRepository
    participant Database

    Client->>API: POST /register (user data)
    API->>UserService: registerUser(userData)
    UserService->>UserLogic: validateUserData(userData)
    UserLogic-->>UserService: validationResult = valid
    UserService->>UserLogic: createUser(userData)
    UserLogic->>UserRepository: save(newUser)
    UserRepository->>Database: insert(newUser)
    Database-->>UserRepository: confirmSave
    UserRepository-->>UserLogic: savedUser
    UserLogic-->>UserService: createdUser
    UserService-->>API: userCreatedResponse
    API-->>Client: Created (user details)
```

## Place Creation
```mermaid
sequenceDiagram
    participant Client
    participant API as API Gateway
    participant PlaceService
    participant PlaceLogic
    participant UserLogic
    participant PlaceRepository
    participant Database

    Client->>API: POST /places (place data)
    API->>PlaceService: createPlace(placeData, userId)
    PlaceService->>UserLogic: verifyUserPermissions(userId)
    UserLogic-->>PlaceService: permissionResult = true
    PlaceService->>PlaceLogic: validatePlaceData(placeData)
    PlaceLogic-->>PlaceService: validationResult = valid
    PlaceService->>PlaceLogic: createPlace(placeData)
    PlaceLogic->>PlaceRepository: save(newPlace)
    PlaceRepository->>Database: insert(newPlace)
    Database-->>PlaceRepository: confirmSave
    PlaceRepository-->>PlaceLogic: savedPlace
    PlaceLogic-->>PlaceService: createdPlace
    PlaceService-->>API: placeCreatedResponse
    API-->>Client: Created (place details)
```

## Review Submission
```mermaid
sequenceDiagram
    participant Client
    participant API as API Gateway
    participant ReviewService
    participant ReviewLogic
    participant PlaceLogic
    participant ReviewRepository
    participant Database

    Client->>API: POST /places/{placeId}/reviews (review data)
    API->>ReviewService: submitReview(reviewData, userId, placeId)
    ReviewService->>PlaceLogic: verifyPlaceExists(placeId)
    PlaceLogic-->>ReviewService: placeExistsResult = true
    ReviewService->>ReviewLogic: validateReviewData(reviewData)
    ReviewLogic-->>ReviewService: validationResult = valid
    ReviewService->>ReviewLogic: createReview(reviewData, userId, placeId)
    ReviewLogic->>ReviewRepository: save(newReview)
    ReviewRepository->>Database: insert(newReview)
    Database-->>ReviewRepository: confirmSave
    ReviewRepository-->>ReviewLogic: savedReview
    ReviewLogic-->>ReviewService: createdReview
    ReviewService-->>API: reviewCreatedResponse
    API-->>Client: Created (review details)
```

## Fetching a List of Places
```mermaid
sequenceDiagram
    participant Client
    participant API as API Gateway
    participant PlaceService
    participant PlaceLogic
    participant PlaceRepository
    participant Database

    Client->>API: GET /places?criteria=value
    API->>PlaceService: getPlaces(criteria)
    PlaceService->>PlaceLogic: validateCriteria(criteria)
    PlaceLogic-->>PlaceService: validationResult = valid
    PlaceService->>PlaceRepository: findPlaces(criteria)
    PlaceRepository->>Database: query(criteria)
    Database-->>PlaceRepository: placeResults
    PlaceRepository-->>PlaceService: placeList
    PlaceService->>PlaceLogic: formatPlaceList(placeList)
    PlaceLogic-->>PlaceService: formattedPlaceList
    PlaceService-->>API: placeListResponse
    API-->>Client: OK (list of places)
```


## User Registration
This sequence diagram illustrates the process of successful user registration in the HBnB application.

#### Key steps:

Client sends registration data to API Gateway

UserService validates user data

UserLogic creates new user

UserRepository saves user to database

Confirmation sent back to client

The Presentation Layer (API Gateway) receives the initial request and delegates to the Business Logic Layer (UserService, UserLogic) for validation and user creation. The Persistence Layer (UserRepository, Database) handles data storage. This flow ensures proper validation and secure storage of new user data.

## Place Creation
This diagram shows the successful creation of a new place listing.

#### Key steps:

Client sends place data to API Gateway

PlaceService verifies user permissions

PlaceLogic validates place data and creates new place

PlaceRepository saves place to database

Confirmation sent back to client

The Presentation Layer initiates the process, while the Business Logic Layer handles permission checks, data validation, and place creation. The Persistence Layer manages data storage. This flow ensures only authorized users can create valid place listings.

## Review Submission
This sequence illustrates the successful submission of a review for a place.

#### Key steps:

Client sends review data to API Gateway

ReviewService verifies place exists

ReviewLogic validates review data and creates new review

ReviewRepository saves review to database

Confirmation sent back to client

The Presentation Layer receives the review submission, the Business Logic Layer verifies the place and validates the review, and the Persistence Layer stores the new review. This process ensures reviews are only submitted for existing places and contain valid data.

## Fetching a List of Places
This diagram depicts the successful retrieval of a list of places based on specified criteria.

#### Key steps:

Client requests places with criteria

PlaceService validates criteria

PlaceRepository queries database for matching places

PlaceLogic formats place list

Formatted list sent back to client

The Presentation Layer receives the initial request, the Business Logic Layer validates the search criteria and formats the results, while the Persistence Layer performs the database query. This flow ensures efficient and accurate retrieval of place listings based on user-specified criteria.