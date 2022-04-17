from flask import Blueprint

# Creates a blueprint for all our code under main
database = Blueprint('database', __name__)

import views
