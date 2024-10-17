from flask import Flask, request, jsonify, redirect, url_for, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from functools import wraps
import os
import re  # For password validation

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness_website.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))  
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

# Route for signup with password validation rules
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Validate input
    if not username or not email or not password:
        return jsonify({'message': 'All fields are required!', 'success': False}), 400

    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'User already exists!', 'success': False}), 400

    # Password validation rules
    if len(password) < 8:
        return jsonify({'message': 'Password must be at least 8 characters long.', 'success': False}), 400
    if not re.search(r"[A-Z]", password):
        return jsonify({'message': 'Password must contain at least one uppercase letter.', 'success': False}), 400
    if not re.search(r"[a-z]", password):
        return jsonify({'message': 'Password must contain at least one lowercase letter.', 'success': False}), 400
    if not re.search(r"[0-9]", password):
        return jsonify({'message': 'Password must contain at least one number.', 'success': False}), 400
    if not re.search(r"[@$!%*#?&]", password):
        return jsonify({'message': 'Password must contain at least one special character.', 'success': False}), 400


    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')  
    

    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully!', 'success': True})

# Route for login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Validate input
    if not email or not password:
        return jsonify({'message': 'Email and password are required!', 'success': False}), 400


    user = User.query.filter_by(email=email).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        session['user_id'] = user.id  
        return jsonify({'message': 'Login successful!', 'success': True})
    else:
        return jsonify({'message': 'Invalid email or password!', 'success': False}), 401


@app.route('/diet')
@login_required
def diet():
    return send_from_directory('static', 'diet.html')

# Route for logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)  
    return redirect(url_for('home'))  

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
