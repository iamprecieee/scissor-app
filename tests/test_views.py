import pytest
from scissor.models import Url, CustomUrl

def test_home(client, db):
    response = client.get("/home", follow_redirects=True)
    assert response.status_code == 200


def post_and_assert(client, url, data, model, filters):
    response = client.post(url, data=data, follow_redirects=True)
    assert response.status_code == 200
    instance = model.query.filter_by(**filters).first()
    assert instance is not None
    return response, instance

def test_shortenurl(client, db):
    response = client.post("/shortenurl", data=dict(
        text="https://www.example.com",
    ), follow_redirects=True)
    url = Url.query.filter_by(original_url="https://www.example.com").first()
    assert url is not None
    assert response.status_code == 200

def test_customurl(client, db):
    response = client.post("/customurl", data=dict(
        text="https://www.example.com",
        text2="custom"
    ), follow_redirects=True)
    url = CustomUrl.query.filter_by(original_url="https://www.example.com").first()
    assert url is not None
    assert url.custom_short_url == "custom"
    assert response.status_code == 200
