from flask import Flask, render_template

app = Flask(__name__)

places = [
    {"id": 1, "name": "Beach House", "image": "places_photos/beach_house.jpg", "description": "A nice house on the beach with a nice view !"},
    {"id": 2, "name": "Cabin in the mountains", "image": "places_photos/mountain_cabin.jpg", "description": "Sleep under the beautiful sky of the mountains !"},
    {"id": 3, "name": "Modern apartment", "image": "places_photos/modern_apartment.jpg", "description": "Luxury apartment in the center of the city."},
    {"id": 4, "name": "Cabin in the forest", "image": "places_photos/forest_cabin.jpg", "description": "Cozy cabin in the woods."},
    {"id": 5, "name": "Apartment in the center", "image": "places_photos/apartment_center.jpg", "description": "Simple apartment in the center of the city."},
    {"id": 6, "name": "Traditional house", "image": "places_photos/trad_house.jpg", "description": "Traditional house in the countryside."},
    {"id": 7, "name": "Castle", "image": "places_photos/castle.jpg", "description": "Rent a room inside a medieval castle."},
    {"id": 8, "name": "Villa", "image": "places_photos/villa.jpg", "description": "Villa near the city center."}
]

@app.route('/')
def main_route():
    return render_template('index.html', places=places)

@app.route('/index.html')
def index_route():
    return render_template('index.html', places=places)

@app.route('/place.html')
def place_route():
    return render_template('place.html')

@app.route('/add_review.html')
def review_route():
    return render_template('add_review.html')

@app.route('/login.html')
def login_route():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True, port=5500)
