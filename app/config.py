import os

#SQLALCHEMY
SQLALCHEMY_ENGINES = {
    'default': os.getenv('DATABASE_URI', 'postgresql://username:password@localhost/dbname')
}
SQLALCHEMY_TRACK_MODIFICATIONS = False

# ALembic
ALEMBIC = {
    'script_location': '../migrations'
}

#JWT
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret')
JWT_VERIFY_SUB = False