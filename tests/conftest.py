import pytest

from app import create_app
from app.extensions import db, Base
from app.models import User

@pytest.fixture()
def app():
    """Create application for testing"""
    app = create_app('test_config.py')
    
    with app.app_context():
        engine = db.engine
        Base.metadata.create_all(engine)
        yield app
        db.session.reset()
        Base.metadata.drop_all(engine)
        
@pytest.fixture()
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture()
def runner(app):
    """Create test CLI runner"""
    return app.test_cli_runner()