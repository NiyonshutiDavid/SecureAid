from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import db, bcrypt
from .models import User, Donations
from .forms import RegistrationForm, LoginForm, DonationForm

# Create a Blueprint for your routes
views = Blueprint('views', __name__)

@views.route('/')
def landing_page():
    return render_template('Landing_page.html')

@views.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('views.landing_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            first_name=form.firstname.data,
            last_name=form.lastname.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash("Your account was successfully created, you can log in now", 'success')
        return redirect(url_for("views.login"))
    return render_template('signup_page.html', form=form)

@views.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.landing_page'))
    form = LoginForm()
    next_page = request.args.get("next")
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            if next_page:
                return redirect(next_page)
            return redirect(url_for('views.user_dashboard'))
        else:
            flash("Login is unsuccessful. Check your email and password", 'warning')
    return render_template('login_page.html', form=form)

@views.route('/dashboard')
@login_required
def user_dashboard():
    """Display user dashboard when a user is authenticated"""
    return render_template('user_dashboard.html', user=current_user)

@views.route('/donate_to_project')
@login_required
def donate_to_project():
    """Display user dashboard when a user clicks donate to a project"""
    return render_template('Donation_page.html', user=current_user)

@views.route('/donate', methods=['GET', 'POST'])
@login_required
def donate():
    donations = Donations.query.all()  # Fetch all donations to display
    if request.method == 'POST':
        donation_id = request.form.get('donation_id')
        donation_amount = request.form.get('donation_amount')

        # Assuming you have an Order model defined elsewhere
        # Create an order - make sure 'Order' model is defined in models.py if this is needed
        # new_order = Order(user_id=current_user.id, donation_id=donation_id, donation_amount=donation_amount)
        # db.session.add(new_order)
        # db.session.commit()

        flash('Donation made successfully!', 'success')
        return redirect(url_for('views.donate'))

    return render_template('Donation_page.html', donations=donations)
