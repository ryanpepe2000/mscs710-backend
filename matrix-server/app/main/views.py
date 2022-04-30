import logging
from . import main
from flask import render_template, redirect, url_for, flash

logger = logging.getLogger(__name__.split(".", 1)[1])


@main.route('/', methods=['GET'])
def main_page():
    logger.debug("Rendering index.html template")
    return render_template('index.html'), 200


@main.route('/about', methods=['GET'])
def about_page():
    logger.info("Rendering about.html template")
    return render_template('main/about.html'), 200
