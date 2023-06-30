import pytest
from flask import url_for
from werkzeug.security import generate_password_hash

from scissor import create_app, db
from scissor.models import User

@pytest.fixture
def test_client():
    flask_app = create_app('testing')

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


@pytest.fixture
def init_database():
    db.create_all()

    # Add test data
    test_user = User(username='testuser', email='test@example.com', password=generate_password_hash('testpassword', method='sha256'))
    db.session.add(test_user)
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()


def test_valid_login(test_client, init_database):
    response = test_client.post(url_for('auth.login'),
                                data=dict(identifier='testuser', password='testpassword'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Good to have you back' in response.data


def test_valid_signup(test_client, init_database):
    response = test_client.post(url_for('auth.sign_up'),
                                data=dict(username='newuser', email='newuser@example.com', password1='newpassword', password2='newpassword'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Account created!' in response.data

def test_valid_logout(test_client, init_database):
    # login user
    test_client.post(url_for('auth.login'), data=dict(identifier='testuser', password='testpassword'), follow_redirects=True)
    
    response = test_client.get(url_for('auth.logout'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Logged out successfully!' in response.data


def test_shorten_url(test_client, init_database):
    test_client.post(url_for('auth.login'), data=dict(identifier='testuser', password='testpassword'), follow_redirects=True)

    response = test_client.post(url_for('views.shortenurl'), data=dict(text='https://www.example.com'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Post created!' in response.data

def test_custom_url(test_client, init_database):
    test_client.post(url_for('auth.login'), data=dict(identifier='testuser', password='testpassword'), follow_redirects=True)

    response = test_client.post(url_for('views.customurl'), data=dict(text='https://www.example.com', text2='customurl'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Post created!' in response.data
