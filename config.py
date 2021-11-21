import os


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY')


class ProductionConfig(Config):
    HOST = os.getenv('host')
    DATABASE = os.getenv('database')
    USER = os.getenv('user')
    PASSWORD = os.getenv('password')
    PORT = os.getenv('port')


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = 'secret'
    DATABASE = 'LogCoronaTestDB.db'
