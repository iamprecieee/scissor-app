from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app as app, send_file
from flask_login import login_required, current_user
from .models import Url, CustomUrl
from . import db
import random, string, urllib.parse, qrcode, io, requests, logging 
from functools import wraps

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
        result = urllib.parse.urlparse(url)
        if all([result.scheme, result.netloc]):
            response = requests.get(url)
            return response.status_code == 200
        return False
    except ValueError:
        return False

@views.route("/")
@views.route("/home")
def home():
    print("Home function triggered")
    urls = Url.query.all()
    custom_urls = CustomUrl.query.all()
    return render_template("home.html", user = current_user, urls = urls, custom_urls=custom_urls, server_name=app.config['SERVER_NAME'])

@views.route("/shortenurl", methods=['GET', 'POST'])
@login_required
@limit("10 per minute")
def shortenurl():
    if request.method == "POST":
        text = request.form.get('text')
        if not text:
            logger.error('Text cannot be empty')
        else:
            original_url = text
            if not validate_url(original_url):
                logger.error('Invalid URL')
                return render_template("shortenurl.html")
            else:
                short_url = generate_short_url()
                existing_url = Url.query.filter_by(original_url=original_url).first()
                if existing_url is not None:
                    logger.error('URL already exists!')
                    return render_template("shortenurl.html")
                else:
                    new_url = Url(original_url=original_url, short_url=short_url, user_id=current_user.id)
                    db.session.add(new_url)
                    db.session.commit()
                    logger.info('Post created!')
                    return redirect(url_for('views.home'))
    return render_template("shortenurl.html")

@views.route("/customurl", methods=['GET', 'POST'])
@login_required
@limit("10 per minute")
def customurl():
    if request.method == "POST":
        text = request.form.get('text')
        text2 = request.form.get('text2')
        if not text or not text2:
            logger.error('Text fields cannot be empty')
        else:
            original_url = text
            if not validate_url(original_url):
                logger.error('Invalid URL')
                return render_template("customurl.html")
            custom_short_url = text2
            existing_url = CustomUrl.query.filter_by(original_url=original_url).first()
            if existing_url is not None:
                logger.error('URL already exists!')
                return render_template("customurl.html")
            else:
                new_url = CustomUrl(original_url=original_url, custom_short_url=custom_short_url, user_id=current_user.id)
                db.session.add(new_url)
                db.session.commit()
                logger.info('Post created!')
                return redirect(url_for('views.home'))
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
        flash('Invalid URL', category='error')
        return redirect(url_for('views.home'))

@views.route('/generate_qr/<url_key>')
@login_required
@limit("10 per minute")
def generate_qr(url_key):
    """ Generates QR code """
    url = Url.query.filter_by(short_url=url_key).first()
    if url is None:
        url = CustomUrl.query.filter_by(custom_short_url=url_key).first()
    if not url or url.user_id != current_user.id:
        flash('Invalid URL', category='error')
        return redirect(url_for('views.home'))
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=1,
    )
    qr.add_data('http://' + app.config['SERVER_NAME'] + '/' +url_key)
    qr.make(fit=True)
    img = qr.make_image(fill='blue', back_color="white")
    # Save QR code image to a bytes buffer
    image_buffer = io.BytesIO()
    img.save(image_buffer)
    image_buffer.seek(0)
    return send_file(image_buffer, mimetype='image/png')
