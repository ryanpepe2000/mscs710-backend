"""
Configuration Settings for the Matrix Server. Switch between configurations by setting
the ENV variable within the Flask config object in your CLI.

MacOS
export FLASK_ENV='development'

Windows
set FLASK_ENV='development'

@date 3.16.21
@author Christian Saltarelli
"""
from os import environ, path, remove
from pathlib import Path
from dotenv import load_dotenv
from logging.config import fileConfig

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """ Default Configuration Settings """
    SECRET_KEY = environ.get('SECRET_KEY')

    # Logging Configuration
    log_dir = Path('logs/')

    if path.exists(log_dir / 'out.log'):
        remove(log_dir / 'out.log')

    fileConfig(log_dir / 'logging.ini', disable_existing_loggers=False)

    # Disable tracking to save on memory and performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = environ.get('MYSQL_DEVELOPMENT_URI')

    # AWS ECS
    # TODO:- Implement AWS Credentials through dotenv


class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = environ.get('MYSQL_DEVELOPMENT_URI')
    SQLAlchemy_ECHO = True


class TestingConfig(Config):
    FLASK_ENV = 'testing'
    DEBUG = True
    TESTING = True
    BCRYPT_HASHING_ROUNDS = 4
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = environ.get('MYSQL_TESTING_URI')
