from . import database
from ..models import *


@database.route('/create-db')
def create_db():
    # Test database stuff
    db.create_all()
    db.session.commit()
    return "Success"


@database.route('/delete-db')
def delete_db():
    # Test database stuff
    db.drop_all()
    db.session.commit()
    return "Dropped"
