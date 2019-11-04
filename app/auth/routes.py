"""
Contains routes used for authenticating User
"""
from flask import render_template, redirect, url_for, flash, request, current_app
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Route for registering a user
    """
    if current_user.is_authenticated:
        current_app.logger.debug(
            "{} is already registered".format(current_user))
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        current_app.logger.info("Registered user {}".format(user))
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route for logging in
    """
    if current_user.is_authenticated:
        current_app.logger.debug(
            "{} is already authenticated".format(current_user))
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():  # if form is valid
        user = User.query.filter_by(username=form.username.data).first()
        # if user exist and passowrd correct
        if user is None or not user.check_password(form.password.data):
            current_app.logger.info("{} failed login".format(user))
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        # if next argument sent. From @login_required
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        current_app.logger.debug("Next from login {}".format(next))
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    """
    Route for logging out a user
    """
    current_app.logger.debug("{} loged out".format(current_user))
    logout_user()
    return redirect(url_for('main.index'))
