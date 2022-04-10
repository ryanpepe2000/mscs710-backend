"""
Initialization settings for launching the Matrix Server. Developed utilizing the
application factory pattern.

@date 3.16.22
@author Christian Saltarelli
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Global References
db = SQLAlchemy()
bcrypt = None
login_manager = None


def init_app():
    global bcrypt, login_manager

    """ Initialize the Matrix Server """
    app = Flask(__name__, instance_relative_config=True, static_folder='static')

    if app.config['ENV'] == 'production':
        app.config.from_object('config.ProductionConfig')
    elif app.config['ENV'] == 'testing':
        app.config.from_object('config.TestingConfig')
    else:
        app.config.from_object('config.DevelopmentConfig')

    # Initialize Plugins
    db.init_app(app)
    bcrypt = Bcrypt(app)
    login_manager = LoginManager(app)

    # Import these AFTER initializing the database to avoid circular imports
    from app.main import main
    from app.database import database
    from app.agent import agent
    from app.auth import auth

    # Register Blueprints
    app.register_blueprint(main)
    app.register_blueprint(database)
    app.register_blueprint(agent)
    app.register_blueprint(auth)

    # Configure Authentication Plugins
    login_manager.login_view = "login_page"
    login_manager.login_message_category = "info"

    return app
