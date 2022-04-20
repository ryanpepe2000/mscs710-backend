"""
Configuration settings for the PyTest Framework with all necessary definitions
for PyTest Fixtures used across all test cases.

@date 4.15.22
@author Christian Saltarelli
"""
import pytest
from ..app import init_app, db, models


@pytest.fixture(scope='module')
def test_client():
    matrix_app = init_app()

    # Get Test Context of App
    testing_client = matrix_app.test_client()

    # Establish Application Context
    ctx = matrix_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


@pytest.fixture(scope='module')
def init_database():
    # Create our Testing Database
    db.create_all()

    yield db

    db.drop_all()


@pytest.fixture(scope='module')
def test_user():
    user = models.User('test@gmail.com', 'testtesttest')
    return user


@pytest.fixture(scope='module')
def test_device():
    device = models.Device('test_device')
    return device

