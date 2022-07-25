class BaseConfig(object):
    DEBUG = False
    TESTING = False

    # configuring secret key
    SECRET_KEY = '479366fd70548d7cdc02ac54f4eb8943c2e5b7176f09438e08155b355dcad51e'

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
    MAIL_DEFAULT_SENDER = 'national.projects.library@gmail.com'
    MAIL_USERNAME = 'national.projects.library@gmail.com'
    MAIL_PASSWORD = 'butndqvnuzfjongw'


class TestingConfig(BaseConfig):
    TESTING = True
