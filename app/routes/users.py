from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models import User
from app.extensions import db

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    user = db.get_or_abort(User, id)
    return jsonify(user.to_json())

@users_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    user = db.get_or_abort(User, current_user_id)
    return jsonify(user.to_json(include_email=True))

@users_bp.route('/me/edit', methods=['PUT'])
@jwt_required()
def edit_current_user():
    current_user_id = get_jwt_identity()
    user = db.get_or_abort(User, current_user_id)
    
    data = request.get_json()
    allowed_fields = [
        'display_name', 'bio', 'location',
        'website', 'profile_picture_url', 'cover_photo_url'
    ]
    
    updated_fields = []

    for field in allowed_fields:
        if field in data:
            value = data[field]
            if value is not None and value != '':
                setattr(user, field, data[field])
                updated_fields.append(field)
            elif value is None:
                setattr(user, field, None)
                updated_fields.append(field)
    
    if not updated_fields:
        return jsonify(message='No valid fields to update'), 400

    try:
        db.session.commit()
        return jsonify(
            message='User updated successfully',
            user=user.to_json(include_email=True)
        ), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(message='Update failed', error=str(e)), 500