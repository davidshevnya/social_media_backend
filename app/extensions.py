from flask_sqlalchemy_lite import SQLAlchemy
from flask_alembic import Alembic
from flask_jwt_extended import JWTManager
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy()
alembic = Alembic(metadatas=Base.metadata)
jwt = JWTManager()