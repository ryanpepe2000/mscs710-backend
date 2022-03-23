from wsgi import app
from . import main


@main.route('/')
def hello_world():
    app.logger.debug("TESTING DEBUG LOG FUNCTIONALITY")
    return "Hello, world!"
