from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from flask_bcrypt import Bcrypt
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .forms import RegistrationForm, LoginForm

auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            flash('Logged in successfully!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.user_dashboard'))
        else:
            flash('Login failed. Check your email and password.', category='error')

    return render_template("login_page/index.html", form=form, user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(email=email, first_name=first_name, last_name=last_name, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.user_dashboard'))

    return render_template("signup page/index.html", form=form, user=current_user)

