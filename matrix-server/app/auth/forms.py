"""
Encapsulates all required forms that will be used for authentication within
the Matrix Systems client pages. Such forms contained are account registration
and account login.

@date 4.6.22
@author Christian Saltarelli
"""
import logging, re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from ..models import User

logger = logging.getLogger(__name__.split(".", 1)[1])


class RegistrationForm(FlaskForm):
    def validate_email(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()

        if email:
            raise ValidationError(f'Email is already in use. Please try a different email address.')

    def validate_password(self, password_to_check):
        regex = re.compile('[_!#$%^&*()<>?/|}"\/{~:]')
        result = regex.search(password_to_check.data)

        if result.group():
            raise ValidationError(f'Illegal character "{result.group()}" not allowed. Please try again.')

    # Registration Fields
    first_name = StringField(label='First name', validators=[DataRequired()])
    last_name = StringField(label='Last name', validators=[DataRequired()])
    email = StringField(label='Email address', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=12), DataRequired()])
    password_conf = PasswordField(label='Password confirmation', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    email = StringField(label='Email address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Login')