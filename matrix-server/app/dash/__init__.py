from flask import Blueprint

# Create our Blueprint for Authentication views
dash = Blueprint('dash', __name__)

from . import views