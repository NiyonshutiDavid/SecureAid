from flask import render_template, redirect, url_for, flash, request
from SecureAid_app import app, db, bcrypt
from SecureAid_app.models import Users, Donations, Order
from SecureAid_app.forms import RegistrationForm, LoginForm, DonationForm
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
def landing_page():
    return render_template('Landing page/index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = Users(first_name=form.first_name.data,
                         last_name=form.last_name.data,
                         email=form.email.data,
                         password=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup page/index.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('user_dashboard'))
        else:
            flash('Login failed. Check your email and password.', 'danger')
    
    return render_template('Login_page/index.html', form=form)

@app.route('/dashboard')
@login_required
def user_dashboard():
    return render_template('user_dashboard/index.html', user=current_user)

@app.route('/donate', methods=['GET', 'POST'])
@login_required
def donate():
    donations = Donations.query.all()  # Fetch all donations to display
    if request.method == 'POST':
        donation_id = request.form.get('donation_id')
        donation_amount = request.form.get('donation_amount')
        
        new_order = Order(user_id=current_user.id, donation_id=donation_id, donation_amount=donation_amount)
        db.session.add(new_order)
        db.session.commit()
        
        flash('Donation made successfully!', 'success')
        return redirect(url_for('donate'))
    
    return render_template('donating_page.html', donations=donations)

@app.route('/my_donations')
@login_required
def my_donations():
    user_orders = Order.query.filter_by(user_id=current_user.id).all()  # Fetch user orders
    return render_template('my_donations_page.html', orders=user_orders)
