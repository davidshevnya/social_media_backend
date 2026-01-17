from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required,
    get_jwt_identity
)
from flasgger import swag_from
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import select

from app.models import User
from app.extensions import db
from app.schemas import user_schema
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - username
            - email
            - password
          properties:
            username:
              type: string
              example: johndoe
            email:
              type: string
              format: email
              example: john@example.com
            password:
              type: string
              format: password
              example: SecurePass123
    responses:
      201:
        description: User created successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: User created successfully
      400:
        description: Validation failed
        schema:
          type: object
          properties:
            message:
              type: string
              example: Validation failed.
            errors:
              type: object
      409:
        description: Email or username already exists
        schema:
          type: object
          properties:
            message:
              type: string
              example: That email already exists
      500:
        description: Server error
        schema:
          type: object
          properties:
            message:
              type: string
              example: Create failed
            error:
              type: string
    """
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if db.session.scalar(select(User).where(User.email == email)):
        return jsonify(message='That email already exists'), 409
    elif db.session.scalar(select(User).where(User.username == username)):
        return jsonify(message='That username already exists'), 409
    
    password_hash = generate_password_hash(password)
    data.pop('password')
    
    try:
        validation = user_schema.load(data, session=db.session)
        user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        return jsonify(message='User created succesfully'), 201
    except ValidationError as e:
        return jsonify(message='Validation failed.', errors=e.messages_dict), 400
    except Exception as e:
        db.session.rollback()
        return jsonify(message='Create failed', error=str(e)), 500
    

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User Log in
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - password
          properties:
            username:
              type: string
              example: johndoe
            email:
              type: string
              format: email
              example: john@example.com
            password:
              type: string
              format: password
              example: SecurePass123
    responses:
      200:
        description: Successful login
        schema:
          type: object
          properties:
            message:
              type: string
              example: Login Successful
            access_token:
              type: string
              example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
            refresh_token:
              type: string
              example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
      401:
        description: Failed logging in
        schema:
          type: object
          properties:
            message:
              type: string
              example: Bad email or username.
    """
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
    """
    JWT refresh token
    ---
    tags:
      - Authentication
    parameters:
      - name: Authorization
        in: header
        required: true
        description: Bearer JWT refresh token
    responses:
      200:
        description: Success
        schema:
            type: object
            properties:
                access_token:
                    type: string
                    example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    """
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)