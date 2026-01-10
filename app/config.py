import os

#SQLALCHEMY
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql://username:password@localhost/dbname')
SQLALCHEMY_TRACK_MODIFICATIONS = False

#JWT
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret')