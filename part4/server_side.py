from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main_route():
    return render_template('index.html')

@app.route('/index.html')
def index_route():
    return render_template('index.html')

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
