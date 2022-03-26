import logging
from . import main

logger = logging.getLogger(__name__)


@main.route('/')
def hello_world():
    logger.debug("TESTING DEBUG LOG FUNCTIONALITY")
    return "Hello, world!"
