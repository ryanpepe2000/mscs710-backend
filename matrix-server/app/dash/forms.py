"""
Encapsulates all required forms that will be used for registering new devices within
the system.

@date 4.6.22
@author Ryan Pepe
"""
import logging
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from ..models import Device
from flask_login import current_user

logger = logging.getLogger(__name__)


class DeviceRegistrationForm(FlaskForm):
    def validate_device_name(self, device_name_to_check):
        registered_device = Device.query.filter_by(user_id=current_user.id, device_name=device_name_to_check.data).first()

        if registered_device:
            if registered_device.device_name.lower() == device_name_to_check.data.lower():
                raise ValidationError(
                    f'Device name is already in use for your account. Please provide a different name')

    # Device Registration Fields
    device_name = StringField(label='Device name', validators=[DataRequired()])
    submit = SubmitField(label='Register Device')
