from datetime import datetime
from datetime import UTC
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models import Post, User
from app.extensions import db
from app.schemas import post_schema

posts_bp = Blueprint('posts', __name__, url_prefix='/posts')

@posts_bp.route('/create', methods=['POST'])
@jwt_required()
def create_post():
    data = request.json
    current_user_id = get_jwt_identity()

    content = data.get('content')
    if not content:
        return jsonify(message='Content is required'), 400
    
    title = data.get('title')

    try:
        post = Post(title=title, content=content, user_id=current_user_id)
        db.session.add(post)
        db.session.commit()

        return jsonify(message='Post created successfully!', post=post_schema.dump(post)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify(message='Failed to create post')
    
@posts_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_post(id):
    post = db.get_or_abort(Post, id)
    return jsonify(message='Success', post=post_schema.dump(post))

@posts_bp.route('/<int:id>/edit', methods=['PUT'])
@jwt_required()
def edit_post(id):
    post = db.get_or_abort(Post, id)
    data = request.get_json()
    
    allowed_fields = [
        'title', 'content'
    ]
    
    updated_fields = []

    for field in allowed_fields:
        if field in data:
            value = data[field]
            if value is not None and value != '':
                setattr(post, field, data[field])
                updated_fields.append(field)
            elif value is None:
                setattr(post, field, None)
                updated_fields.append(field)
    
    if not updated_fields:
        return jsonify(message='No valid fields to update'), 400

    post.updated_at = datetime.now(UTC)
    
    try:
        db.session.commit()
        return jsonify(
            message='Post updated successfully',
            post=post_schema.dump(post)
        ), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(message='Update failed', error=str(e)), 500
    
@posts_bp.route('/user/<int:id>', methods=['GET'])
@jwt_required()
def get_user_posts(id):
    user = db.get_or_abort(User, id)
    return jsonify(message='Success', posts=post_schema.dump(user.posts, many=True))