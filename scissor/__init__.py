from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import secrets, os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
DB_NAME = "database.db"


def create_app(config_name=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
    app.config['JWT_SECRET_KEY'] = secrets.token_urlsafe(16)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    

    app.config['SERVER_NAME'] = os.getenv('SERVER_NAME', 'scissor-app.onrender.com')

    db.init_app(app)
    migrate.init_app(app, db)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    
    global cache
    cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://localhost:6379/0'})
    
    global limiter
    limiter = Limiter(key_func=get_remote_address, app=app, storage_uri="redis://localhost:6379/0")

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
