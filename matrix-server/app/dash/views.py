import logging
from . import dash
from .. import db
from ..models import User, DeviceAssignment, Device
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user

logger = logging.getLogger(__name__)


@dash.route('/dashboard', methods=['GET'])
def dashboard_page():

    if current_user.is_authenticated:
        # Check for Registered Devices (if any)
        user_devices = DeviceAssignment.query.filter_by(user_id=current_user.id).all()

        if len(user_devices) > 0:
            logger.info("I think we may have found some devices")
        else:
            logger.info("Recognized No Devices!")
            return render_template('dash/dashboard.html', devices=None, metrics=None)

    else:
        # User must log in to view the Dashboard
        flash(f'Please login to view the dashboard.', category='info')
        return redirect(url_for('auth.login_page')), 301
