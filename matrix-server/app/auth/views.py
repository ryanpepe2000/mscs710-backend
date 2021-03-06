import logging
from . import auth
from . import forms
from .. import db
from .. import util
from ..models import User, UserRole, Role
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user

logger = logging.getLogger(__name__.split(".", 1)[1])


@auth.route('/register', methods=['GET', 'POST'])
def register_page():
    register_form = forms.RegistrationForm()

    if request.method == "POST":
        # Registration Submit
        if register_form.validate_on_submit():
            # Insert New User to Database
            new_user = User(first_name=register_form.first_name.data,
                            last_name=register_form.last_name.data,
                            email=register_form.email.data,
                            password=register_form.password.data)
            db.session.add(new_user)
            db.session.commit()

            logger.info(f'Committing new Registered User Account: {new_user.email}')

            # TESTING PURPOSES
            new_role = Role(role_name='User', role_desc='Basic User Role')
            db.session.add(new_role)
            db.session.commit()

            # Attach Default Role to New User Record
            new_user_role = UserRole(role_id=new_role.role_id, user_id=new_user.id)
            db.session.add(new_user_role)
            db.session.commit()

            # Update Login Manager for Authenticated User
            login_user(new_user)

            # Update User on Account Creation
            logging.info("Rendering dashboard.html template")
            flash(f'Account created successfully! You are now logged in.', category='success')
            return redirect(url_for('dash.dashboard_page')), 301

        if register_form.errors != {}:
            for err_msg in register_form.errors.values():
                flash(f'{util.clean_error_msg(err_msg[0])}', category='danger')

    logger.debug("Rendering register.html template")
    return render_template('auth/register.html', form=register_form), 200


@auth.route('/login', methods=['GET', 'POST'])
def login_page():
    login_form = forms.LoginForm()

    if request.method == 'POST':
        if login_form.validate_on_submit():
            attempted_user = User.query.filter_by(email=login_form.email.data).first()

            if attempted_user and attempted_user.validate_password(attempted_password=login_form.password.data):
                login_user(attempted_user)

                # Redirect to Dashboard Page
                flash(f'You are now logged in.', category='success')
                return redirect(url_for('dash.dashboard_page')), 301
            else:
                logger.warning(f'Invalid login attempt for user ({login_form.email.data}) from {request.remote_addr}')
                flash(f'The email or password given was incorrect. Please try again.', category='danger')

    return render_template('auth/login.html', form=login_form), 200


@auth.route('/logout', methods=['GET'])
def logout_page():
    logout_user()

    flash(f'You have been logged out.', category='info')
    return redirect(url_for('main.main_page')), 301
