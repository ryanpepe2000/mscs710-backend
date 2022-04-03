import logging
from . import main
from flask import render_template, redirect, url_for

logger = logging.getLogger(__name__)


@main.route('/')
def hello_world():
    logger.debug("Rendering index.html template")
    return render_template('index.html')
