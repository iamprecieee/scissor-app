import pytest
from scissor import create_app, db as _db

@pytest.fixture
def app():
    _app = create_app("test")
    return _app

@pytest.fixture
def db(app):
    with app.app_context():
        _db.create_all()
        yield _db
        _db.drop_all()