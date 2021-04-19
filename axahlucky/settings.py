# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')

    DEBUG_TB_INTERCEPT_REDIRECTS = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AXAHLUCKY_OPINION_PER_PAGE = 10
    AXAHLUCKY_KEYWORD_PER_PAGE = 20

    AXAHLUCKY_SLOW_QUERY_THRESHOLD = 1

    BOOTSTRAP_SERVE_LOCAL = True

    MAIL_USE_SSL = True
    MAIL_PORT = 465

    AXAHLUCKY_MAIL_SUBJECT_PREFIX = '[AxahLucky]'
    ADMIN_EMAIL_ADDRESS = os.getenv('ADMIN_EMAIL_ADDRESS')





class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = \
        os.getenv('DATABASE_URL_DEV', prefix + os.path.join(basedir, 'data-dev.db'))
    REDIS_URL = "redis://localhost"
    MAIL_SERVER = os.getenv('MAIL_SERVER_DEV')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME_DEV')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD_DEV')
    MAIL_DEFAULT_SENDER = ('AXAHLUCKY', os.getenv('MAIL_USERNAME_DEV'))


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'  # in-memory database

    MAIL_SERVER = os.getenv('MAIL_SERVER_TEST')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME_TEST')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD_TEST')
    MAIL_DEFAULT_SENDER = ('AXAHLUCKY', os.getenv('MAIL_USERNAME_TEST'))


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        prefix + os.path.join(basedir, 'data.db'))
    
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('AXAHLUCKY', os.getenv('MAIL_USERNAME'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
