class BaseConfig(object):
    DEBUG = False
    TESTING = False

    # configuring secret key
    SECRET_KEY = 'put a random alphanumeric string here'

    # configuration of mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True


class ProductionConfig(BaseConfig):
    pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True

    # configuration of database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # configuration of mail
    MAIL_DEFAULT_SENDER = 'some email address here'
    MAIL_USERNAME = 'some email address here'
    MAIL_PASSWORD = 'password of mail here'


class TestingConfig(BaseConfig):
    TESTING = True
