
from flask import Blueprint, render_template, redirect, url_for, request, session, current_app as app, render_template_string
from . import db, mail, cache
from .models import User, PasswordHistory
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from requests_oauthlib import OAuth2Session
import requests
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message


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
            session['message'] = f"Good to have you back {user.username}!"
            session['message_type'] = 'success'
            return redirect(url_for("views.dashboard"))
        else:
            session['message'] = 'Invalid Credentials!'
            session['message_type'] = 'error'
            message = session.pop('message')
            message_type = session.pop('message_type')
            return render_template("login.html", message=message, message_type=message_type)
    message = None
    message_type = None
    if 'message' in session:
        message = session.pop('message')
        message_type = session.pop('message_type')
    return render_template("login.html", message=message, message_type=message_type)

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
            session['message'] = 'Email already exists!'
            session['message_type'] = 'error'
        elif password1 != password2:
            session['message'] = 'Password does not match!'
            session['message_type'] = 'error'
        elif len(password1) < 8:
            session['message'] = 'Password is too short!'
            session['message_type'] = 'error'
        elif len(email) < 5:
            session['message'] = 'Invalid email!'
            session['message_type'] = 'error'
        else:
            new_user = User(username=username, email=email, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            session['message'] = 'Account created!'
            session['message_type'] = 'success'
            login_user(new_user, remember=True)
            return redirect(url_for("views.dashboard"))
    message = None
    message_type = None
    if 'message' in session:
        message = session.pop('message')
        message_type = session.pop('message_type')
    return render_template("signup.html", message=message, message_type=message_type)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    session['message'] = 'Logged out successfully!'
    session['message_type'] = 'success'
    return redirect(url_for("views.home"))

@auth.route('/initiate_password_reset', methods=['POST'])
@limit("10 per minute")
def initiate_password_reset(email=None):
    if not email:
        email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    if user:
        # create a token with the user's email
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        token = serializer.dumps(email, salt='email-confirm')

        # create a password reset link with the token
        reset_link = url_for('auth.reset_password', token=token, _external=True)

        # create an email message
        message_template = '''
        <html>
        <body style="color: lime; background-color: black;">
            <h1>Scissor</h1>
            <p>Hi {{ username }},</p>
            <p>Let's reset your password so you can get back to shortening.</p>
            <p><a href="{{ reset_link }}" style="display:inline-block; border: 2px solid lime; color: lime; background-color: transparent; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; border-radius: 15px; transition: all 0.5s;">Reset Password</a></p>
            <p>If you did not ask to reset your password, please ignore this message.</p>
            <p>The Scissor team</p>
            <br>
            <p>This message was mailed to [{{ email }}] by the scssr.tech team.</p>
        </body>
        </html>
        '''

        # Render the template with the necessary variables
        message_body = render_template_string(message_template, username=user.username, reset_link=reset_link, email=email)

        # create an email message
        msg = Message('Password Reset Request',
                      sender='noreply@scssr.tech',
                      recipients=[email])
        msg.body = message_body
        msg.html = message_body
        # send the email
        try:
            with mail.connect() as connection:
                connection.send(msg)
            session['message'] = 'An email has been sent with instructions to reset your password!'
            session['message_type'] = 'success'
        except Exception:
            session['message'] = 'Failed to send reset email!'
            session['message_type'] = 'error'
        return redirect(url_for("auth.login"))
    else:
        session['message'] = 'Email not found!'
        session['message_type'] = 'error'
        return redirect(url_for("auth.login"))

@auth.route("/forgot_password", methods=['GET', 'POST'])
@limit("10 per minute")
def forgot_password():
    if request.method == 'POST':
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()
        if user:
            # Construct the authorization URL for Google OAuth 2.0
            authorization_base_url = "https://accounts.google.com/o/oauth2/auth"
            client_id = app.config['CLIENT_ID']
            redirect_uri = app.config['REDIRECT_URI']
            scope = ["openid", "email", "profile"]

            oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
            authorization_url, state = oauth.authorization_url(authorization_base_url)

            # Save the state and email in the session for use in the callback route
            session['oauth_state'] = state
            session['reset_email'] = email

            # Redirect the user to the Google authorization URL
            return redirect(authorization_url)
        else:
            session['message'] = 'Email not found!'
            session['message_type'] = 'error'
            return redirect(url_for("auth.login"))
    return render_template("forgot_password.html")

@auth.route("/oauth_callback")
@limit("10 per minute")
@cache.cached(timeout = 50)
def oauth_callback():
    authorization_base_url = "https://accounts.google.com/o/oauth2/auth"
    token_url = app.config['TOKEN_URL']
    client_id = app.config['CLIENT_ID']
    client_secret = app.config['CLIENT_SECRET']
    redirect_uri = app.config['REDIRECT_URI']

    # Verify the state to prevent CSRF attacks
    if 'oauth_state' not in session or request.args.get('state') != session.pop('oauth_state', None):
        session['message'] = 'Invalid OAuth state.'
        session['message_type'] = 'error'
        return redirect(url_for("auth.login"))

    # Get the authorization code from the query parameters
    code = request.args.get('code')

    # Exchange the authorization code for an access token
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri)
    token = oauth.fetch_token(token_url, code=code, client_secret=client_secret)

    # Get the reset email from the session
    email = session.pop('reset_email', None)

    if token and email:
        # Send a request to Google's userinfo endpoint to get the user's email
        userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        headers = {
            "Authorization": f"Bearer {token['access_token']}"
        }
        response = requests.get(userinfo_url, headers=headers)
        if response.status_code == 200:
            user_info = response.json()
            # Verify that the email associated with the access token matches the reset email
            if user_info['email'] == email:
                return initiate_password_reset(email)
            else:
                session['message'] = 'OAuth email does not match the reset email.'
                session['message_type'] = 'error'
        else:
            session['message'] = 'Failed to get user information.'
            session['message_type'] = 'error'
    else:
        session['message'] = 'Failed to obtain an access token.'
        session['message_type'] = 'error'
    return redirect(url_for("auth.login"))

@auth.route("/reset_password/<token>", methods=['GET', 'POST'])
@limit("10 per minute")
@cache.cached(timeout = 50)
def reset_password(token):
    try:
        email = app.serializer.loads(token, salt='email-confirm', max_age=3600)
    except:
        session['message'] = 'Invalid or expired token!'
        session['message_type'] = 'error'
        return redirect(url_for("auth.login"))
    user = User.query.filter_by(email=email).first()
    if request.method == 'POST':
        password = request.form.get("password")
        new_password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        if user:
            # Check if the new password hash is in the last X password hashes
            last_passwords = PasswordHistory.query.filter_by(user_id=user.id).order_by(PasswordHistory.timestamp.desc()).limit(3)
            for past_password in last_passwords:
                if check_password_hash(past_password.password_hash, password):
                    session['message'] = 'New password cannot be the same as one of the previous passwords!'
                    session['message_type'] = 'error'
                    return redirect(url_for("auth.login"))
            # Add the new password to the password history
            new_password = PasswordHistory(user_id=user.id, password_hash=new_password_hash)
            db.session.add(new_password)
            user.password = new_password_hash
            db.session.commit()
            session['message'] = 'Your password has been updated!'
            session['message_type'] = 'success'
            return redirect(url_for("auth.login"))
        else:
            session['message'] = 'User not found!'
            session['message_type'] = 'error'
            return redirect(url_for("auth.login"))
    return render_template("reset_password.html")
