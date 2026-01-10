from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import User
from app.extensions import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if User.query.filter_by(email=email).first():
        return jsonify(message='That email already exists'), 409
    elif User.query.filter_by(username=username).first():
        return jsonify(message='That username already exists'), 409
    
    password_hash = generate_password_hash(password)
    user = User(username=username, email=email, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()
    return jsonify(message='User created succesfully'), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if username:
        user = User.query.filter_by(username=username).first()
    elif email:
        user = User.query.filter_by(email=email).first()
    else:
        return jsonify(message='Enter username or email'), 401
    
    if not user:
        return jsonify(message='Bad email or username. User doesnt exist.'), 401
    
    if not check_password_hash(user.password_hash, password):
        return jsonify(message='Bad password.'), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify(message='Login Successful', access_token=access_token)