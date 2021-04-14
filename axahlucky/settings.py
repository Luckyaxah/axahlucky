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
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AXAHLUCKY_OPINION_PER_PAGE = 10
    AXAHLUCKY_KEYWORD_PER_PAGE = 10
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')



class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = \
        os.getenv('DATABASE_URL_DEV', prefix + os.path.join(basedir, 'data-dev.db'))
    REDIS_URL = "redis://localhost"


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'  # in-memory database


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        prefix + os.path.join(basedir, 'data.db'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
