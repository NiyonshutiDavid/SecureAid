from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import db, bcrypt
from .models import User, Donations
from .forms import RegistrationForm, LoginForm, DonationForm

# Create a Blueprint for your routes
views = Blueprint('views', __name__)

@views.route('/')
def landing_page():
    return render_template('Landing Page/index.html')

@views.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        email=form.email.data,
                        password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('views.login'))

    return render_template('signup_page/index.html', form=form)

@views.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('views.user_dashboard'))
        else:
            flash('Login failed. Check your email and password.', 'danger')

    return render_template('login_page/index.html', form=form)

@views.route('/dashboard')
@login_required
def user_dashboard():
    return render_template('user_dashboard/index.html', user=current_user)

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

    return render_template('my_donations_page.html', donations=donations)

