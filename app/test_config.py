#sqlalchemy
TESTING = True
SQLALCHEMY_ENGINES = {
    'default': 'sqlite:///:memory'
}
SQLALCHEMY_TRACK_MODIFICATIONS = False

# ALEMBIC
ALEMBIC = {
    'script_location': '../migrations'
}

#jwt
JWT_SECRET_KEY = 'test-secret-keyKlM2254'
JWT_VERIFY_SUB = False