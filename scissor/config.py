import os
class Config:
    SECRET_KEY = 'e70e6a4a54fda890589dd01577b5d751'
    SQLALCHEMY_DATABASE_URI = "postgres://scissordb_spvj_user:FT7PUU4WbJUPVMfrX9OvDSphje0f15OZ@dpg-cieupudgkuvq1o2o2pjg-a.oregon-postgres.render.com/scissordb_spvj"
    SERVER_NAME = os.getenv("SERVER_NAME", '127.0.0.1:5000')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.getenv("REDIS_URL")
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = REDIS_URL
    CACHE_DEFAULT_TIMEOUT = 300
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = 'Sender Name <scssr.tech@gmail.com>'
    TOKEN_URL = os.getenv("TOKEN_URL")
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    REDIRECT_URI = os.getenv("REDIRECT_URI")
    MYSTERY_DATA = os.getenv("MYSTERY_DATA")
    MYSTERY = os.getenv("MYSTERY")

    
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
