"""
Configuration settings for the PyTest Framework with all necessary definitions
for PyTest Fixtures used across all test cases.

@date 4.15.22
@author Christian Saltarelli
"""
import pytest
from app import init_app, db, models


@pytest.fixture(scope='module')
def test_client():
    matrix_app = init_app()

    # Get Test Context of App
    testing_client = matrix_app.test_client()

    # Establish Application Context
    ctx = matrix_app.app_context()
    ctx.push()

    yield testing_client

    # Pop Application Context
    ctx.pop()


@pytest.fixture(scope='function')
def init_database():
    # Create our Testing Database
    db.create_all()

    yield db

    db.session.close()

    db.drop_all()


@pytest.fixture(scope='function')
def test_user(init_database):
    user = models.User(first_name='John',
                       last_name='Smith',
                       email='test@gmail.com',
                       password='testtesttest')
    init_database.session.add(user)
    init_database.session.commit()

    return user


@pytest.fixture(scope='function')
def test_device(init_database):
    device = models.Device(machine_name='test machine')
    init_database.session.add(device)
    init_database.session.commit()

    return device


