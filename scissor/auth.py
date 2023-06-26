from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app as app
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from functools import wraps


auth = Blueprint("auth", __name__)

def limit(key):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            limiter = app.limiter.limit(key)
            return limiter(f)(*args, **kwargs)
        return decorated_function
    return decorator

@auth.route("/login", methods=['GET', 'POST'])
@limit("10 per minute")
def login():
    if request.method == 'POST':
        identifier = request.form.get("identifier")
        password = request.form.get("password")
        user = User.query.filter((User.email==identifier )| (User.username==identifier)).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            flash(f"Good to have you back {user.username}", category='success')
            return redirect(url_for('views.home'))
        else:
            flash('Email/Username does not exist.', category='error')
    return render_template("login.html")

@auth.route("/signup", methods=['GET', 'POST'])
@limit("10 per minute")
def sign_up():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        email_exists = User.query.filter_by(email=email).first()
        if email_exists:
            flash('Email already exists!', category='error')
        elif password1 != password2:
            flash('Password does not match.', category='error')
        elif len(password1) < 8:
            flash('Password is too short.', category='error')
        elif len(email) < 5:
            flash('Invalid email.', category='error')
        else:
            new_user = User(username=username, email=email, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!')
            login_user(new_user, remember=True)
            return redirect(url_for("views.home"))
    return render_template("signup.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', category='success')
    return redirect(url_for("views.home"))
