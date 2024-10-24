from flask import Flask, request, jsonify, redirect, url_for, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from functools import wraps
import pandas as pd
import pickle
import os

# Load the model and scaler
with open('kmeans_model.pkl', 'rb') as f:
    kmeans = pickle.load(f)

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

app = Flask(__name__)

# SQLite Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness_website.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Home route
@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

# Sign-up route
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Input validation
    if not username or not email or not password:
        return jsonify({'message': 'All fields are required!', 'success': False}), 400

    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'User already exists!', 'success': False}), 400

    # Hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Create and store new user
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully!', 'success': True})

# Login route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Input validation
    if not email or not password:
        return jsonify({'message': 'Email and password are required!', 'success': False}), 400

    # Authenticate user
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        session['user_id'] = user.id
        return jsonify({'message': 'Login successful!', 'success': True})
    else:
        return jsonify({'message': 'Invalid email or password!', 'success': False}), 401

# Diet recommendations route (requires login)
@app.route('/recommend', methods=['POST'])
@login_required
def recommend():
    user_goal = request.json.get('goal')

    try:
        df_cleaned = pd.read_csv("df_cleaned.csv")
    except FileNotFoundError:
        return jsonify({'message': 'Internal error: dataset not found', 'success': False}), 500

    nutritional_columns = df_cleaned.select_dtypes(include=['float64', 'int64']).columns
    X_scaled = scaler.transform(df_cleaned[nutritional_columns])
    df_cleaned['Cluster'] = kmeans.predict(X_scaled)

    goal_mapping = {
        'muscle gain': 0,
        'fat burn': 1,
        'maintenance': 2,
    }

    goal_cluster = goal_mapping.get(user_goal)
    if goal_cluster is None:
        return jsonify({'message': 'Invalid goal!', 'success': False}), 400

    recommendations = df_cleaned[df_cleaned['Cluster'] == goal_cluster].to_dict(orient='records')
    
    return jsonify({'recommendations': recommendations, 'success': True})

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully!', 'success': True})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
