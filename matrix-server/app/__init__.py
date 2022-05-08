"""
Initialization settings for launching the Matrix Server. Developed utilizing the
application factory pattern.

@date 3.16.22
@author Christian Saltarelli
"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Global References
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


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
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Import these AFTER initializing the database to avoid circular imports
    from app.main import main
    from app.database import database
    from app.agent import agent
    from app.auth import auth
    from app.dash import dash

    # Register Blueprints
    app.register_blueprint(main)
    app.register_blueprint(database)
    app.register_blueprint(agent)
    app.register_blueprint(auth)
    app.register_blueprint(dash)

    # Register Error Handling Routes
    app.register_error_handler(404, page_not_found)

    # Configure Authentication Plugins
    login_manager.login_view = "login_page"
    login_manager.login_message_category = "info"

    return app


def page_not_found(error):
    return render_template('404.html'), 404
