from . import db 
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    username = db.Column(db.String(150), unique = False)
    password = db.Column(db.String(150))
    urls = db.relationship('Url', backref='user', lazy=True)
    custom_urls = db.relationship('CustomUrl', backref='user', lazy=True)

class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), unique=True, nullable=False)
    short_url = db.Column(db.String(120), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    click_count = db.Column(db.Integer, default=0)

class CustomUrl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), unique=True, nullable=False)
    custom_short_url = db.Column(db.String(120), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    click_count = db.Column(db.Integer, default=0)