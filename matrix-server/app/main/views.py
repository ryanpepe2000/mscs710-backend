import logging
from os import path
from . import main
from flask import render_template, redirect, url_for, flash

logger = logging.getLogger(__name__.split(".", 1)[1])


@main.route('/', methods=['GET'])
def main_page():
    logger.debug("Rendering index.html template")
    return render_template('index.html')


@main.errorhandler(404)
def page_not_found():
    return "Page does not exist", 404
