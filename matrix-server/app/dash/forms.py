"""
Encapsulates all required forms that will be used for registering new devices within
the system.

@date 4.6.22
@author Ryan Pepe
"""
import logging
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from ..models import User

logger = logging.getLogger(__name__)


class DeviceRegistrationForm(FlaskForm):
    # Registration Fields
    device_name = StringField(label='Device name', validators=[DataRequired()])
    submit = SubmitField(label='Register Device')
