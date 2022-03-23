from . import database
from .. import db


@database.route('/create-db')
def create_db():
    # Test database stuff
    db.create_all()
    return "Success"


@database.route('/delete-db')
def delete_db():
    # Test database stuff
    db.drop_all()
    return "Dropped"
