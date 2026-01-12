#sqlalchemy
TESTING = True
SQLALCHEMY_ENGINES = {
    'default': 'sqlite:///:memory'
}
SQLALCHEMY_TRACK_MODIFICATIONS = False

#jwt
JWT_SECRET_KEY = 'test-secret-keyKlM2254'
JWT_VERIFY_SUB = False