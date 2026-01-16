import re
from marshmallow import validates, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.fields import Nested


from app.models import User, Post

class PostSchema(SQLAlchemyAutoSchema):
    
    class Meta:
        model = Post
        load_instance = True
        include_fk = True
        include_relationships = True
        exclude = ('user', )

   
    @validates('content')
    def validate_content(self, value, data_key):
        if not value or len(value) < 3:
            raise ValidationError('Content must be at least 3 characters long')

    
class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_relationships = True
        exclude = ('password_hash', 'posts')
    
    @validates('username')
    @validates('display_name')
    @validates('location')
    def validate_user(self, value, data_key):
        if not value or len(value.rstrip()) < 3:
            raise ValidationError(f'{data_key} must be at least 3 characters long')
    
    @validates('email')
    def validate_email(self, value, data_key):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise ValidationError("Invalid email format")
    
    @validates('profile_picture_url')
    @validates('cover_photo_url')
    @validates('website')
    def validate_url(self, value, data_key):
        url_regex = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$'
        if not re.match(url_regex, value):
            raise ValidationError("Invalid URL format")

class PublicUserSchema(SQLAlchemyAutoSchema):
    class Meta(UserSchema.Meta):
        exclude = ('email', )

user_schema = UserSchema() # type: ignore
public_user_schema = PublicUserSchema()
post_schema = PostSchema()