from datetime import datetime
from datetime import UTC
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app.models import Post, User
from app.extensions import db
from app.schemas import post_schema

posts_bp = Blueprint('posts', __name__, url_prefix='/posts')

@posts_bp.route('/create', methods=['POST'])
@jwt_required()
def create_post():
    data = request.json
    data['user_id'] = get_jwt_identity()

    try:
        validation = post_schema.load(data, session=db.session)
        post = Post(**data)
        db.session.add(post)
        db.session.commit()

        return jsonify(
            message='Post created successfully!',
            post=post_schema.dump(post)
        ), 201
    except ValidationError as e:
        return jsonify(
            message='Validation failed.',
            errors=e.messages_dict
        ), 400
    except Exception as e:
        db.session.rollback()
        return jsonify(
            message='Failed to create post',
            error=str(e)
        ), 500

@posts_bp.route('/<int:id>/delete', methods=['DELETE'])
@jwt_required()
def delete_post(id):
    post = db.get_or_abort(Post, id)
    try:
        db.session.delete(post)
        db.session.commit()
        return jsonify(message='Post deleted successfully!')
    except Exception as e:
        db.session.rollback()
        return jsonify(message='Deleting failed', error=str(e))

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
        data = post_schema.dump(post)
        validation = post_schema.load(data, session=db.session) # type: ignore
        db.session.commit()
        return jsonify(
            message='Post updated successfully',
            post=post_schema.dump(post)
        ), 200
    except ValidationError as e:
        return jsonify(
            message='Validation failed.',
            errors=e.messages_dict
        ), 400
    except Exception as e:
        db.session.rollback()
        return jsonify(
            message='Update failed',
            error=str(e)
        ), 500
    
@posts_bp.route('/user/<int:id>', methods=['GET'])
@jwt_required()
def get_user_posts(id):
    user = db.get_or_abort(User, id)
    return jsonify(message='Success', posts=post_schema.dump(user.posts, many=True))