from . import main


@main.route('/')
def hello_world():
    main.logger.debug("TESTING DEBUG LOG FUNCTIONALITY")
    return "Hello, world!"
