import logging
from . import dash, forms
from .. import db, util
from ..models import Device
from ..metrics import Metrics, ChartMetrics
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user

logger = logging.getLogger(__name__.split(".", 1)[1])


@dash.route('/dashboard', methods=['GET'])
def dashboard_page():
    if current_user.is_authenticated:
        # Check for Registered Devices (if any)
        user_devices = Device.query.filter_by(user_id=current_user.id).all()

        if user_devices is not None and len(user_devices) > 0:
            # Get First Device Ref
            device_ref = user_devices[0]

            # Query all metrics
            metrics = Metrics(device_ref)

            logger.info(f"Metric Validation Outcome: {metrics.is_valid()}")

            if metrics.is_valid():
                chart_data = ChartMetrics(metrics)
            else:
                metrics = None
                chart_data = None

            flash(f'Now viewing metrics collected for {device_ref.device_name}', category='info')
            return render_template('dash/dashboard.html', devices=user_devices, current_device=device_ref.device_name,
                                   metrics=metrics, chart_data=chart_data, conv_bytes=util.bytes_to_amt_per_sec), 200
        else:
            return render_template('dash/dashboard.html', devices=None, current_device=None,
                                   metrics=None, chart_data=None, conv_bytes=util.bytes_to_amt_per_sec), 200

    else:
        # User must log in to view the Dashboard
        flash(f'Please login to view the dashboard.', category='info')
        return redirect(url_for('auth.login_page')), 301


@dash.route('/dashboard/<string:device_name>', methods=['GET'])
def dashboard_device_page(device_name):
    if current_user.is_authenticated:
        device_ref = Device.query.filter_by(device_name=device_name, user_id=current_user.id).first()

        # Validate Requested Device is Owned by current_user
        if device_ref is not None:
            # Get Total Device List
            user_devices = Device.query.filter_by(user_id=current_user.id).all()

            # Query all metrics
            metrics = Metrics(device_ref)

            logger.info(f"Metric Validation Outcome: {metrics.is_valid()}")

            if metrics.is_valid():
                chart_data = ChartMetrics(metrics)
            else:
                metrics = None
                chart_data = None

            flash(f'Now viewing metrics collected for {device_ref.device_name}', category='info')
            return render_template('dash/dashboard.html', devices=user_devices, current_device=device_ref.device_name,
                                   metrics=metrics, chart_data=chart_data, conv_bytes=util.bytes_to_amt_per_sec), 200
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
                # Insert New Device to Database
                new_device = Device(device_name=register_form.device_name.data,
                                    user_id=current_user.id)
                db.session.add(new_device)
                db.session.commit()

                logger.info("Committing new Registered User Device")
                flash(f'Device registered successfully! Now viewing {new_device.device_name}', category='success')
                return redirect(url_for('dash.dashboard_device_page', device_name=new_device.device_name)), 301

            if register_form.errors != {}:
                for err_msg in register_form.errors.values():
                    flash(f'{util.clean_error_msg(err_msg[0])}', category='danger')

        return render_template('dash/register-device.html', form=register_form), 200

    # User must log in to register new devices
    flash(f'Please login to register a new device.', category='info')
    return redirect(url_for('auth.login_page')), 301
