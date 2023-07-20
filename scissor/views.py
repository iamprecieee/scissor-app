from flask import Blueprint, render_template, request, session, redirect, url_for, current_app as app, send_file, jsonify
from flask_login import login_required, current_user
from .models import Url, CustomUrl
from . import db, cache
import random, string, qrcode, io, requests, logging 
from functools import wraps
from urllib.parse import urlparse

views = Blueprint("views", __name__)

def limit(key):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            limiter = app.limiter.limit(key)
            return limiter(f)(*args, **kwargs)
        return decorated_function
    return decorator

#random URL generation
def generate_short_url():
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=6))

# set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# URL Validation with status check
def validate_url(url):
    try:
        parsed_url = urlparse(url)
        if all([parsed_url.scheme, parsed_url.netloc]):
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception if the request was not successful (status code >= 400)
            return True
        return False
    except requests.exceptions.RequestException:
        return False

@views.route("/")
@views.route("/home")
@limit("10 per minute")
@cache.cached(timeout = 10)
def home():
    message = None
    message_type = None
    if 'message' in session:
        message = session.pop('message')
        message_type = session.pop('message_type')
    return render_template("home.html", message=message, message_type=message_type)

@views.route("/dashboard")
@login_required
@limit("10 per minute")
@cache.cached(timeout = 10)
def dashboard():
    urls = Url.query.filter_by(user_id=current_user.id).all()
    custom_urls = CustomUrl.query.filter_by(user_id=current_user.id).all()
    message = None
    message_type = None
    if 'message' in session:
        message = session.pop('message')
        message_type = session.pop('message_type')
    return render_template("dashboard.html", user = current_user, urls = urls, custom_urls=custom_urls, server_name=app.config['SERVER_NAME'], message=message, message_type=message_type)

@views.route("/shortenurl", methods=['GET', 'POST'])
@login_required
@limit("10 per minute")
def shortenurl():
    if request.method == "POST":
        text = request.form.get('text')
        if not text:
            session['message'] = 'Text cannot be empty!'
            session['message_type'] = 'error'
            message = session.pop('message')
            message_type = session.pop('message_type')
            return render_template("shortenurl.html", message=message, message_type=message_type)
        else:
            original_url = text
            if not validate_url(original_url):
                session['message'] = 'Invalid URL!'
                session['message_type'] = 'error'
                message = session.pop('message')
                message_type = session.pop('message_type')
                return render_template("shortenurl.html", message=message, message_type=message_type)
            else:
                short_url = generate_short_url()
                existing_url = Url.query.filter_by(original_url=original_url, user_id=current_user.id).first()
                if existing_url is not None:
                    session['message'] = 'URL already exists!'
                    session['message_type'] = 'error'
                    message = session.pop('message')
                    message_type = session.pop('message_type')
                    return render_template("shortenurl.html", message=message, message_type=message_type)
                else:
                    new_url = Url(original_url=original_url, short_url=short_url, user_id=current_user.id)
                    db.session.add(new_url)
                    db.session.commit()
                    session['message'] = 'Post created!'
                    session['message_type'] = 'success'
                    return redirect(url_for('views.dashboard'))
    return render_template("shortenurl.html")

@views.route("/customurl", methods=['GET', 'POST'])
@login_required
@limit("10 per minute")
def customurl():
    if request.method == "POST":
        text = request.form.get('text')
        text2 = request.form.get('text2')
        if not text or not text2:
            session['message'] = 'Text cannot be empty!'
            session['message_type'] = 'error'
            message = session.pop('message')
            message_type = session.pop('message_type')
            return render_template("customurl.html", message=message, message_type=message_type)
        else:
            original_url = text
            if not validate_url(original_url):
                session['message'] = 'Invalid URL!'
                session['message_type'] = 'error'
                message = session.pop('message')
                message_type = session.pop('message_type')
                return render_template("customurl.html", message=message, message_type=message_type)
            custom_short_url = text2
            existing_url = CustomUrl.query.filter_by(original_url=original_url, user_id=current_user.id).first()
            existing_custom_short_url = CustomUrl.query.filter_by(custom_short_url=custom_short_url, user_id=current_user.id).first()
            existing_short_url = Url.query.filter_by(short_url=custom_short_url, user_id=current_user.id).first()     
            if existing_url is not None:
                session['message'] = 'URL already exists!'
                session['message_type'] = 'error'
                message = session.pop('message')
                message_type = session.pop('message_type')
                return render_template("customurl.html", message=message, message_type=message_type)
            elif existing_custom_short_url is not None:
                session['message'] = 'Custom short URL already in use!'
                session['message_type'] = 'error'
                message = session.pop('message')
                message_type = session.pop('message_type')
                return render_template("customurl.html", message=message, message_type=message_type)
            elif existing_short_url is not None:
                session['message'] = 'Short URL already in use!'
                session['message_type'] = 'error'
                message = session.pop('message')
                message_type = session.pop('message_type')
                return render_template("customurl.html", message=message, message_type=message_type)
            else:
                new_url = CustomUrl(original_url=original_url, custom_short_url=custom_short_url, user_id=current_user.id)
                db.session.add(new_url)
                db.session.commit()
                session['message'] = 'Post created!'
                session['message_type'] = 'success'
                return redirect(url_for('views.dashboard'))
    return render_template("customurl.html")

@views.route('/<url_key>')
@limit("10 per minute")
def redirection(url_key):
    url = Url.query.filter_by(short_url=url_key).first()
    if url is None:  # If no short_url is found, try to find a custom_short_url
        url = CustomUrl.query.filter_by(custom_short_url=url_key).first()
    if url:
        url.click_count += 1
        db.session.commit()
        return redirect(url.original_url)
    else:
        return redirect(url_for('views.dashboard'))

@views.route('/generate_qr/<url_key>')
@login_required
@limit("10 per minute")
def generate_qr(url_key):
    """ Generates QR code """
    url = Url.query.filter_by(short_url=url_key).first()
    if url is None:
        url = CustomUrl.query.filter_by(custom_short_url=url_key).first()
    if not url or url.user_id != current_user.id:
        session['message'] = 'Invalid URL!'
        session['message_type'] = 'error'
        return redirect(url_for('views.dashboard'))
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=1,
    )
    qr.add_data('http://' + app.config['SERVER_NAME'] + '/' +url_key)
    qr.make(fit=True)
    img = qr.make_image(fill_color='lime', back_color='black')
    # Save QR code image to a bytes buffer
    image_buffer = io.BytesIO()
    img.save(image_buffer)
    image_buffer.seek(0)
    return send_file(image_buffer, mimetype='image/png')

@views.route('/<url_key>/delete')
@login_required
@limit("10 per minute")
def delete(url_key):
    url = Url.query.filter_by(short_url=url_key, user_id=current_user.id).first()
    if url is None:
        url = CustomUrl.query.filter_by(custom_short_url=url_key, user_id=current_user.id).first()
    if url:
        db.session.delete(url)
        db.session.commit()
        session['message'] = 'Post deleted!'
        session['message_type'] = 'success'
        return redirect(url_for('views.dashboard'))
    session['message'] = 'Invalid URL!'
    session['message_type'] = 'error'
    return redirect(url_for('views.dashboard'))


@views.route('/<url_key>/edit', methods=['GET', 'POST'])
@login_required
@limit("10 per minute")
def update(url_key):
    custom_url = CustomUrl.query.filter_by(custom_short_url=url_key, user_id=current_user.id).first()
    host = request.host_url
    if custom_url:
        if request.method == 'POST':
            custom_path = request.form['custom_path']
            if custom_path:
                link_exists = CustomUrl.query.filter_by(custom_short_url=custom_path).first()
                link2_exists = Url.query.filter_by(short_url=custom_path).first()
                if link_exists:
                    session['message'] = 'That custom path already exists.'
                    session['message_type'] = 'error'
                    message = session.pop('message')
                    message_type = session.pop('message_type')
                    return render_template('edit.html', url=custom_url, host=host, message=message, message_type=message_type)
                elif link2_exists:
                    session['message'] = 'That short path already exists.'
                    session['message_type'] = 'error'
                    message = session.pop('message')
                    message_type = session.pop('message_type')
                    return render_template('edit.html', url=custom_url, host=host, message=message, message_type=message_type)
                custom_url.custom_short_url = custom_path
                db.session.commit()
                session['message'] = 'Post updated!'
                session['message_type'] = 'success'
                return redirect(url_for('views.dashboard'))
        return render_template('edit.html', url=custom_url, host=host)
    return render_template('dashboard.html')

@views.route("/analytics_data")
@login_required
@limit("10 per minute")
def analytics_data():
    # Get the URLs for the current user
    urls = Url.query.filter_by(user_id=current_user.id).all()
    custom_urls = CustomUrl.query.filter_by(user_id=current_user.id).all()
    # Prepare the data
    data = {
        "labels": [url.short_url for url in urls] + [c_url.custom_short_url for c_url in custom_urls],
        "click_counts": [url.click_count for url in urls] + [c_url.click_count for c_url in custom_urls]
    }
    return jsonify(data)


@views.route("/analytics")
@login_required
@limit("10 per minute")
def analytics():
    return render_template("analytics.html")

