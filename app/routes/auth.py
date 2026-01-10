from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash

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