from flask import Blueprint

# Creates a blueprint for all our code under main
agent = Blueprint('agent', __name__)

from . import views
