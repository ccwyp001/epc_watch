import datetime
import os
from datetime import timedelta

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = True
    SECRET_KEY = 'hard to guess string'
    # JWT SETTING
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'EpcWatch'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    # RESTFUL SETTING
    ERROR_404_HELP = False
    # SQLALCHEMY SETTING
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False



class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY SETTING
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://onekeeper:onekeeper123@127.0.0.1/epc'

    SQLALCHEMY_POOL_SIZE = 100
    SQLALCHEMY_POOL_RECYCLE = 120
    SQLALCHEMY_POOL_TIMEOUT = 20


class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY SETTING
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'develop': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
