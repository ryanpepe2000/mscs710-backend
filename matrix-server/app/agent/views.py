import logging
from flask import request
from . import agent

logger = logging.getLogger(__name__)


@agent.route('/api/send_data', methods=['POST'])
def add_message():
    content = request.get_json()

    logger.debug(content)
    return content, 200
