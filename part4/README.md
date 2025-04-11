# HBnB Evolution

HBnB Evolution is a clone of Airbnb built to simulate an online platform for renting vacation properties. This application has a backend powered by Flask and SQLAlchemy with a frontend made using HTML, CSS, and JavaScript. It mimics key features of Airbnb, including authentication, property listings, and reviews.

## Tech Stack

- **Backend**: Flask, SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (via SQLAlchemy)
- **Authentication**: Token-based authentication using cookies

## Features

- User authentication (login/logout)
- Listing of vacation properties (with images, description, price, and more)
- Viewing property details (including reviews)
- Ability to filter properties by price
- Token-based authentication to manage user login state across pages

## Setup Instructions

### 1. Backend (Flask + SQLAlchemy)

#### Prerequisites:
Make sure you have Python 3 installed on your system.

#### Install Dependencies:
Navigate to the backend folder (where `run.py` is located).

Install the required Python packages:

```bash
pip install -r requirements.txt
```

#### Start the Backend Server:
To start the backend server, run the following command:
```
python3 run.py
```

This will host the backend on http://127.0.0.1:5501.

### 2. Frontend (HTML, CSS, JavaScript)
#### Start the Frontend Server:
Navigate to the frontend folder (where your HTML files are located).

Start a simple HTTP server using Python:
```
python3 -m http.server 5500
```
This will host the frontend on http://127.0.0.1:5500.

### 3. Cookie/Token Management
The token/cookie for user authentication is managed across the entire site. When a user logs in successfully, a token is saved as a cookie and is used for making authenticated requests to the backend (e.g., fetching property listings and details). The token expires after 2 hours.

#### Usage
- Login: Users can log in using their email and password. On successful login, a token is stored in the browser cookies for session management.

- View Listings: After logging in, users can view a list of available properties and filter them by price.

- Property Details: Users can click on any property to view more details, including reviews, price, and amenities.

- Add Reviews: Authenticated users can add reviews to the properties they stay in.

#### API Endpoints
- POST /api/v1/auth/login: Login endpoint (requires email and password).

- GET /api/v1/places/: Fetch all properties (requires a valid token).

- GET /api/v1/places/{id}: Fetch details for a specific property (requires a valid token).

#### Notes
- The backend runs on http://127.0.0.1:5501 and handles API requests, including authentication, fetching properties, and handling user data.

- The frontend runs on http://127.0.0.1:5500 and interacts with the backend via API calls.

- Authentication is managed using cookies and a token-based system, ensuring that users are logged in throughout their session.

- The token is stored as a cookie and expires in 2 hours for security reasons.
