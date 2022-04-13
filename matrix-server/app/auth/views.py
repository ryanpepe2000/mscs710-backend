import logging
from . import auth
from . import forms
from .. import db
from ..models import User, UserRole
from ..models import User
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

logger = logging.getLogger(__name__)


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

            logger.info("Committing new Registered User Account")

            # Attach Default Role to New User Record
            # new_user_role = UserRole(role_id=1, user_id=new_user.user_id)
            # db.session.add(new_user_role)
            # db.session.commit()

            # Update Login Manager for Authenticated User
            login_user(new_user)

            # Update User on Account Creation
            logging.info("Rendering dashboard.html template")
            flash(f'Account created successfully! You are now logged in.', category='success')
            # return redirect(url_for('main_page')), 201
            # return redirect(url_for('dashboard_page')), 201
            return render_template('index.html'), 201

        if register_form.errors != {}:
            for err_msg in register_form.errors.values():
                flash(f'{err_msg}', category='danger')

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
                flash(f'You are now logged in.', category='success')
                # Redirect to Dashboard Page
                redirect(url_for('main.main_page')), 301
            else:
                flash(f'The email or password given was incorrect. Please try again.', category='danger')

    return render_template('auth/login.html', form=login_form), 200


@auth.route('/logout', methods=['GET'])
def logout_page():
    logout_user()
    flash(f'You have been logged out!', category='info')

    return redirect(url_for('main.main_page')), 301

# TODO: TEST LOGIN FUNCTIONALITY AND FINISH UI DESIGN FOR LOGIN PAGE

