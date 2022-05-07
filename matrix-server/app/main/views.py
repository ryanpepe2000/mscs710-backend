import logging
from . import main
from flask import render_template
from flask_login import current_user

logger = logging.getLogger(__name__.split(".", 1)[1])


@main.route('/', methods=['GET'])
def main_page():
    status = current_user.is_authenticated

    logger.debug("Rendering index.html template")
    return render_template('index.html', authenticated=status), 200


@main.route('/about', methods=['GET'])
def about_page():
    logger.info("Rendering about.html template")
    return render_template('main/about.html'), 200
