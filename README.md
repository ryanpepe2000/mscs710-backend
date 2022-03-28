# Matrix-Backend

## Description
Apart of Matrix Systems, this repository encompasses our Backend Server which is responsible for parsing incoming metric data from registered devices, storing formatted data in our data store, and facilitating incoming requests from our users through the Matrix Client. Developed for Marist College Graduate Capstone Project Spring 2022.

## Table of Contents
- [Application Structure](#application-structure)
- [Installation](#installation)
- [Testing](#testing)
- [Technologies](#technologies)
- [Authors](#authors)
- [License](#license)
- [Resources](#resources)

## Application Structure
```
matrix-backend
|   run.py
|   config.py
|
|___app
|   |   __init__.py
|   |   models.py
|   |   parse.py
|   |___agent
|   |   |   __init__.py
|   |   |   views.py
|   |___database
|   |   |   __init__.py
|   |   |   views.py
|   |   |   queries.py
|   |___main
|   |   |   __init__.py
|   |   |   views.py
|___logs
|   |   logging.ini
|   |   out.log
|   
|   requirements.txt
|  .env
|   README.md
|   .gitignore
|   LICENSE
|   wsgi.py
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

# Download Docker via this link if necessary: https://docs.docker.com/get-docker/
# Build the docker files to prep for server start
$ docker build
# Compose Docker to launch web-server and proxy server
$ docker compose up
```

Windows (Local Development)
```bash
Coming soon...
```

##Build System
Docker is the primary system which will be used to manage shipping and running of the application. 
Once the command ```docker compose up``` is issued, both the web-server and proxy server will be running
on the ports specified within the dockerfile. Currently, gunicorn is the web-server host that is utilized
for the backend, but this can easily be configured in the dockerfile. Once the web-server is running, the socket
specified in the dockerfile can be utilized by the device agent to POST data to the web-server through predefined
routes for APIs.


## Testing
```bash
Coming soon...
```

## Technologies
This server was developed utilizing a derivative of the traditional LAMP stack. Within this form we continue to use Linux as our base OS, Apache with the use of the Web Server Gateway Interface (WSGI), MySQL an open-source relational database management system, and Python through the adoption of the Flask Web Framework.

## Authors
This project was developed by the following individuals:
- Christian Saltarelli - [LinkedIn](https://www.linkedin.com/in/casaltarelli/)
- Ryan Pepe - [Linkedin](https://www.linkedin.com)
- Ahmed Sallam - [LinkedIn](https://www.linkedin.com)

## License
The MIT License (MIT)
Copyright (c) 2022 Christian Saltarelli, Ryan Pepe, Ahmed Sallam

## Resources
- [Python Styling Guidelines](https://peps.python.org/pep-0008/)
- [Flask Documentation](https://flask.palletsprojects.com/en/2.0.x/)
- [Flask SQLalchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
