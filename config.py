"""
Configuration Settings for Matrix Backend. Switch between configurations by setting
the ENV variable within the Flask config object in your CLI.

MacOS
export FLASK_ENV='development'

Windows
set FLASK_ENV='development'

@date 3.16.21
@author Christian Saltarelli
"""
import os
from os import environ, path, remove
from pathlib import Path
from dotenv import load_dotenv
from logging.config import fileConfig

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


def generate_mysql_uri(ip, port, username, password, name):
    return "mysql://{username}:{password}@{ip}:{port}/{name}".format(username=username,
                                                                     password=password,
                                                                     ip=ip,
                                                                     port=port,
                                                                     name=name)


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

    # Setting up our database variables
    DATABASE_IP = environ.get('DATABASE_IP') or "127.0.0.1"
    DATABASE_PORT = environ.get('DATABASE_PORT') or "3306"
    DATABASE_USERNAME = environ.get('DATABASE_USERNAME') or "root"
    DATABASE_PASSWORD = environ.get('DATABASE_PASSWORD') or ""
    DATABASE_NAME = environ.get('DATABASE_NAME') or 'matrix'

    SQLALCHEMY_DATABASE_URI = generate_mysql_uri(username=DATABASE_USERNAME,
                                                 password=DATABASE_PASSWORD,
                                                 ip=DATABASE_IP,
                                                 port=DATABASE_PORT,
                                                 name=DATABASE_NAME)


class ProductionConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    # SQLALCHEMY_DATABASE_URI = environ.get('MYSQL_PRODUCTION_URI') or generate_mysql_uri()...

    # AWS ECS
    # TODO:- Implement AWS Credentials through dotenv


class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = environ.get('MYSQL_DEVELOPMENT_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLAlchemy_ECHO = True


class TestingConfig(Config):
    FLASK_ENV = 'testing'
    DEBUG = True
    TESTING = False
