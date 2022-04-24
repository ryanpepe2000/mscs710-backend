import logging
from . import dash
from .. import db
from . import forms
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
            return render_template('dash/dashboard.html', devices=user_devices, current_device=user_devices[0].device_name, metrics=None)
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
        if device_ref is not None and device_ref.is_active:
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


@dash.route('/dashboard/register-device', methods=['GET', 'POST'])
def register_device():
    register_form = forms.DeviceRegistrationForm()
    if current_user.is_authenticated:
        if request.method == "POST":
            # Registration Submit
            if register_form.validate_on_submit():
                # Insert New User to Database
                new_device = Device(device_name=register_form.device_name.data,
                                    is_active=True,
                                    user_id=current_user.id)
                db.session.add(new_device)
                db.session.commit()

                logger.info("Committing new Registered User Device")

                return redirect(url_for('dash.dashboard_page')), 301
        return render_template('dash/register-device.html', form=register_form), 200
    else:
        # User must log in to register new devices
        flash(f'Please login to register a new device.', category='info')
        return redirect(url_for('auth.login_page')), 301
