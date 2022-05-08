from flask import Blueprint

# Create our Blueprint for Authentication views
auth = Blueprint('auth', __name__)

from . import views

