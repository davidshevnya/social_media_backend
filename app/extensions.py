from flask_sqlalchemy_lite import SQLAlchemy
from flask_alembic import Alembic
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy()
alembic = Alembic(metadatas=Base.metadata)
jwt = JWTManager()
ma = Marshmallow()
swagger = Swagger()