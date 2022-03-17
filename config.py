"""
Configuration Settings for Matrix Backend. Switch between configurations by setting
the ENV variable within the Flask config object in your CLI.

MacOS
export FLASK_ENV = 'development'

Windows
set FLASK_ENV = 'development'

@date 3.16.21
@author Christian Saltarelli
"""

from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    """ Default Configuration Settings """
    FLASK_ENV = 'development'
    TESTING = True
    SECRET_KEY = environ.get('SECRET_KEY')


class ProductionConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    #SQLALCHEMY_DATABASE_URI = environ.get('PROD_DATABASE_URI')

    # AWS ECS
    # TODO:- Implement AWS Credentials through dotenv


class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = False
    #SQLALCHEMY_DATABASE_URI = environ.get('DEV_DATABASE_URI')


class TestingConfig(Config):
    FLASK_ENV = 'testing'
    DEBUG = True
    TESTING = False