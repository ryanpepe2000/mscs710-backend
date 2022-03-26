"""
Initialization settings for launching the Matrix Server. Developed utilizing the
application factory pattern.

@date 3.16.21
@author Christian Saltarelli
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Global References
db = SQLAlchemy()


def init_app():
    """ Initialize the Matrix Server """
    app = Flask(__name__, instance_relative_config=True)

    if app.config['ENV'] == 'production':
        app.config.from_object('config.ProductionConfig')
    elif app.config['ENV'] == 'testing':
        app.config.from_object('config.TestingConfig')
    else:
        app.config.from_object('config.DevelopmentConfig')

    # Initialize Plugins
    db.init_app(app)

    # Import these AFTER initializing the database to avoid circular imports
    from app.main import main
    from app.database import database
<<<<<<< HEAD:matrix-server/app/__init__.py
    from app.agent import agent
=======
>>>>>>> edb477daf21c3c5b49605f158a5e2c647bde9623:app/__init__.py

    # Register Blueprints
    app.register_blueprint(main)
    app.register_blueprint(database)
    app.register_blueprint(agent)

    return app