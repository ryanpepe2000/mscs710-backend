import logging
from . import main
from flask import render_template, redirect, url_for, flash

logger = logging.getLogger(__name__)


@main.route('/')
def main_page():
    logger.debug("Rendering index.html template")
    flash(f"What's good in the hood!", category='success')
    return render_template('index.html')
