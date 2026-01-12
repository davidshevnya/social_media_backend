from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required,
    get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import select

from app.models import User
from app.extensions import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if db.session.scalar(select(User).where(User.email == email)):
        return jsonify(message='That email already exists'), 409
    elif db.session.scalar(select(User).where(User.username == username)):
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
        user = db.session.scalar(select(User).where(User.username == username))
    elif email:
        user = db.session.scalar(select(User).where(User.email == email))
    else:
        return jsonify(message='Enter username or email'), 401
    
    if not user:
        return jsonify(message='Bad email or username. User doesnt exist.'), 401
    
    if not check_password_hash(user.password_hash, password):
        return jsonify(message='Bad password.'), 401
    
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    return jsonify(
        message='Login Successful', access_token=access_token,
        refresh_token=refresh_token
    )
    
@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)