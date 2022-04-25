import logging
from . import dash
from .. import db
from ..models import User, Device
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user

logger = logging.getLogger(__name__)


@dash.route('/dashboard', methods=['GET'])
def dashboard_page():
    if current_user.is_authenticated:
        # Check for Registered Devices (if any)
        user_devices = Device.query.filter_by(user_id=current_user.id).all()

        if len(user_devices) > 0:
            logger.info("I think we may have found some devices")

            # TESTING PURPOSES ONLY
            data = [
                ("01-01-2020", 1597),
                ("02-01-2020", 1456),
                ("03-01-2020", 1908),
                ("04-01-2020", 896),
                ("05-01-2020", 755),
                ("06-01-2020", 453),
                ("07-01-2020", 1100),
                ("08-01-2020", 1235),
                ("09-01-2020", 1478)
            ]

            labels = [row[0] for row in data]
            values = [row[1] for row in data]

            return render_template('dash/dashboard.html', devices=user_devices, current_device=user_devices[0].device_name, metrics=None, labels=labels, values=values), 200
        else:
            return render_template('dash/dashboard.html', devices=None, metrics=None), 200

    else:
        # User must log in to view the Dashboard
        flash(f'Please login to view the dashboard.', category='info')
        return redirect(url_for('auth.login_page')), 301


@dash.route('/dashboard/<string:device_name>', methods=['GET'])
def dashboard_device_page(device_name):
    if current_user.is_authenticated:
        device_ref = Device.query.filter_by(device_name=device_name, user_id=current_user.id).first()

        # Validate Requested Device is Owned by current_user
        if device_ref.is_active:
            # Get Total Device List
            user_devices = Device.query.filter_by(user_id=current_user.id).all()

            flash(f'Now viewing metrics collected for {device_ref.device_name}', category='info')
            return render_template('dash/dashboard.html', devices=user_devices, current_device=device_ref.device_name, metrics=None), 200
        else:
            flash(f'Device requested does not exist or the device does not belong to you.', category='danger')
            return "Nope", 404

    else:
        # User must log in to view the Dashboard
        flash(f'Please login to view the dashboard.', category='info')
        return redirect(url_for('auth.login_page')), 301
