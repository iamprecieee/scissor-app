import pytest
from scissor.models import User
from werkzeug.security import check_password_hash, generate_password_hash

def test_signup(client, db):
    response = client.post("/signup", data=dict(
        username="test",
        email="test@example.com",
        password1="testpassword",
        password2="testpassword"
    ), follow_redirects=True)
    user = User.query.filter_by(email="test@example.com").first()
    assert user is not None
    assert check_password_hash(user.password, "testpassword")
    assert response.status_code == 200

    # teardown: delete the user after the test
    db.session.delete(user)
    db.session.commit()

def test_login(client, db):
    hashed_password = generate_password_hash("testpassword")
    user = User(username="test", email="test@example.com", password=hashed_password)
    db.session.add(user)
    db.session.commit()
    response = client.post("/login", data=dict(
        identifier="test@example.com",
        password="testpassword"
    ), follow_redirects=True)
    assert response.status_code == 200
