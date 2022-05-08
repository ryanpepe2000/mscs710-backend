# Matrix Server

## Description
Matrix Systems is a remote metric collection service. This repository encompasses our system which is responsible for collecting & parsing incoming metric data from registered devices, storing formatted data in our data store, and facilitating incoming requests from our users through the Matrix Client. This project was developed for Marist College Graduate Capstone Project Spring 2022.

## Table of Contents
- [Application Structure](#application-structure)
- [Installation](#installation)
- [Build System](#build-system)
- [Testing](#testing)
- [Technologies](#technologies)
- [Authors](#authors)
- [License](#license)
- [Resources](#resources)

## Application Structure
```
matrix-server
|   run.py
|   config.py
|   conftest.py
|
|___app
|   |   __init__.py
|   |   models.py
|   |   metrics.py
|   |___agent
|   |   |   __init__.py
|   |   |   views.py
|   |___auth
|   |   |   __init__.py
|   |   |   forms.py
|   |   |   views.py
|   |___dash
|   |   |   __init__.py
|   |   |   forms.py
|   |   |   views.py
|   |___main
|   |   |   __init__.py
|   |   |   views.py
|   |___static
|   |___templates
|___logs
|   |   logging.ini
|   |   out.log
|___tests
|   |___functional
|   |   |   test_functions.py
|   |___unit
|   |   |   test_units.py
|___node_modules
|   requirements.txt
|   .env
|   .gitignore
|   Dockerfile
|   package.json
|   tailwind.config.js
```

## Installation
MacOS (Local Development)
```bash
# Install Python3 v. 3.7.1 or newer via homebrew (Installs pip + setuptools)
$ brew install python

# Verify pip v. 22.0.4 or newer
$ pip --version

# Download Matrix Backend Repository
$ git clone https://github.com/ryanpepe2000/mscs710-backend.git

# Install Application Dependencies 
$ pip install -r requirements.txt

# Install Docker via this link if necessary: https://docs.docker.com/get-docker/
# Build + Run Docker
$ docker-compose up --build
```

Windows (Local Development)
```bash
Coming soon...
```

## Build System
[Docker](https://docs.docker.com/) is the primary system which will be used to manage shipping and running of the application. 
Once ```docker-compose up --build``` is issued, both the matrix-server and proxy server will be running
on the ports specified within the dockerfile. Currently, [Gunicorn](https://docs.gunicorn.org/en/stable/configure.html) is the web-server host that is utilized for the backend, but this can easily be configured in the dockerfile. Once the matrix-server is running, the port
specified in the dockerfile can be utilized by the device agent to POST data to the web-server through predefined APIs.

## Testing
[PyTest](https://docs.pytest.org/en/7.1.x/) was chosen for our functional and unit testing framework. This framework possesses incredible functionality that enables our developers the ability to evaluate our system under various constraints and situations. Providing us the capability to effectively assess the various use cases and behavior we expect from our system. 

```bash
# Go to the root directory of our service matrix-server
$ cd matrix-server

# Instruct the Matrix Server to run under our testing configuration
$ export FLASK_ENV=testing

# Execute our functional and unit test cases
$ python3 -m pytest -v
```

## Technologies
This server was developed utilizing a derivative of the traditional LAMP stack. Within this form we continue to use Linux as our base OS, Apache with the use of the Web Server Gateway Interface (WSGI) Gunicorn, MySQL an open-source relational database management system, and Python through the adoption of the Flask Web Framework.

## Authors
This project was developed by the following individuals:
- Christian Saltarelli - [LinkedIn](https://www.linkedin.com/in/casaltarelli/)
- Ryan Pepe - [Linkedin](https://www.linkedin.com/in/ryan-pepe-dev/)
- Ahmed Sallam - [LinkedIn](https://www.linkedin.com)

## License
The MIT License (MIT)
Copyright (c) 2022 Christian Saltarelli, Ryan Pepe, Ahmed Sallam

## Resources
- [Python Styling Guidelines](https://peps.python.org/pep-0008/)
- [Flask Documentation](https://flask.palletsprojects.com/en/2.0.x/)
- [Flask SQLalchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [PyTest](https://docs.pytest.org/en/7.1.x/)
- [Docker](https://docs.docker.com/)
