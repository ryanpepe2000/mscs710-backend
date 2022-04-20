"""
Encapsulates all test cases for expected functional
capabilities of Matrix Systems.

@date 4.15.22
@author Christian Saltarelli
"""
import json


def test_get_home_view(test_client):
    """
    GIVEN the Matrix System configured for Testing
    WHEN the '/' route is requested (GET)
    THEN check that the response is valid (200)
    """
    response = test_client.get('/')
    assert response.status_code == 200


def test_post_home_view(test_client):
    """
    GIVEN the Matrix System configured for Testing
    WHEN the '/' route is requested (POST)
    THEN check that the response is valid (405)
    """
    response = test_client.post('/')
    assert response.status_code == 405


def test_get_register_view(test_client):
    """
    GIVEN the Matrix System configured for Testing
    WHEN the '/register' route is requested (GET)
    THEN check that the response is valid (200)
    """
    response = test_client.get('/register')
    assert response.status_code == 200


def test_post_register_view(test_client, init_database):
    """
    GIVEN the Matrix System configured for Testing
    WHEN the '/register' route is requested (POST)
    THEN check that the response is valid (200)
    """
    data = {
        'first_name': 'Jim',
        'last_name': 'Smith',
        'email': 'test@gmail.com',
        'password': 'testtesttest',
        'password_conf': 'testtesttest'
    }

    response = test_client.post('/register',
                                data=json.dumps(data),
                                content_type='application/json',
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Account created successfully!' in response.data


def test_get_login_view(test_client, init_database):
    """
    GIVEN the Matrix System configured for Testing
    WHEN the '/login' route is requested (GET)
    THEN check that the response is valid (200)
    """
    response = test_client.get('/login')
    assert response.status_code == 200


def test_post_login_view(test_client, init_database):
    """
    GIVEN the Matrix System configured for Testing
    WHEN the '/login' route is requested (POST)
    THEN check that the response is valid (200)
    """
    data = {
        'first_name': 'Jim',
        'last_name': 'Smith',
        'email': 'test@gmail.com',
        'password': 'testtesttest',
        'password_conf': 'testtesttest'
    }

    # Register for an Account through Test Server + Logout
    response = test_client.post('/register',
                                data=json.dumps(data),
                                content_type='application/json',
                                follow_redirects=True)
    response = test_client.get('/logout')

    # Validate Login POST Functionality
    data = {
        'email': 'test@gmail.com',
        'password': 'testtesttest'
    }

    response = test_client.post('login',
                                data=json.dumps(data),
                                content_type='application/json',
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'You are now logged in.' in response.data


def test_get_logout_view(test_client, init_database):
    """
    GIVEN the Matrix System configured for Testing
    WHEN the '/logout' route is requested (POST)
    THEN check that the response is valid (200)
    """
    data = {
        'first_name': 'Jim',
        'last_name': 'Smith',
        'email': 'test@gmail.com',
        'password': 'testtesttest',
        'password_conf': 'testtesttest'
    }

    # Register for an Account through Test Server + Logout
    response = test_client.post('/register',
                                data=json.dumps(data),
                                content_type='application/json',
                                follow_redirects=True)

    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'You have been logged out!' in response.data


def test_post_logout_view(test_client, init_database):
    """
    GIVEN the Matrix System configured for Testing
    WHEN the '/logout' route is requested (POST)
    THEN check that the response is valid (405)
    """
    response = test_client.post('/logout')
    assert response.status_code == 405


def test_get_dashboard_view_unauthenticated(test_client, init_database):
    """
    GIVEN the Matrix System configured for Testing
    WHEN the '/dashboard' route is requested (GET)
    THEN check that the response is valid for unauthenticated users (301)
    """
    response = test_client.get('/dashboard')
    assert response.status_code == 301


def test_get_dashboard_view_authenticated(test_client, init_database):
    """
    GIVEN the Matrix System configured for Testing
    WHEN the '/dashboard' route is requested (GET)
    THEN check that the response is valid for authenticated users
    """
    data = {
        'first_name': 'Jim',
        'last_name': 'Smith',
        'email': 'test@gmail.com',
        'password': 'testtesttest',
        'password_conf': 'testtesttest'
    }

    # Register for an Account through Test Server
    response = test_client.post('/register',
                                data=json.dumps(data),
                                content_type='application/json',
                                follow_redirects=True)

    response = test_client.get('dashboard')
    assert response.status_code == 200
    assert b'Matrix - Dashboard' in response.data


def test_post_dashboard_view(test_client, init_database):
    """
    GIVEN the Matrix System configured for Testing
    WHEN the '/dashboard' route is requested (POST)
    THEN check that the response is valid (405)
    """
    response = test_client.post('/dashboard')
    assert response.status_code == 405


def test_post_collect_api(test_client, init_database):
    """
    GIVEN the Matrix System configure for Testing
    WHEN the '/api/send_data' route is requested (POST)
    THEN check that the response is valid (200)
    """
    data = {
        "hello": "world"
    }
    response = test_client.post('api/send_data',
                                json=json.dumps(data))
    assert response.status_code == 200


def test_get_collect_api(test_client, init_database):
    """
    GIVEN the Matrix System configured for Testing
    WHEN the '/api/send_data' route is requested (GET)
    THEN check that the response is valid (405)
    """
    response = test_client.get('/api/send_data')
    assert response.status_code == 405


def test_get_404_view(test_client):
    """
    GIVEN the Matrix System configured for Testing
    WHEN a non-existent route is requested (GET)
    THEN check that the response is valid (404)
    """
    response = test_client.get('/random')
    assert response.status_code == 404
