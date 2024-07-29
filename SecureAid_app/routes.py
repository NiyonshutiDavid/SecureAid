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
