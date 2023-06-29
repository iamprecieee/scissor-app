from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from flask_migrate import Migrate
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail 

from .config import Config

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    # This is for generating tokens
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    app.serializer = serializer

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    
    cache = Cache(app, config={
        'CACHE_TYPE': app.config['CACHE_TYPE'], 
        'CACHE_REDIS_URL': app.config['CACHE_REDIS_URL']
    })
    app.cache = cache

    limiter = Limiter(key_func=get_remote_address, app=app, storage_uri=app.config['REDIS_URL'])
    app.limiter = limiter


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User


    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    with app.app_context():
        db.create_all()

    return app
