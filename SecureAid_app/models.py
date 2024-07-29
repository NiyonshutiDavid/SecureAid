from datetime import datetime
from SecureAid_app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)  # Increased length for hashed password
    orders = db.relationship('Order', backref='user', lazy=True)

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', first_name='{self.first_name}', last_name='{self.last_name}')>"

class Donations(db.Model):
    __tablename__ = 'donations'
    id = db.Column(db.Integer, primary_key=True)
    donation_name = db.Column(db.String(50), nullable=False, unique=True)
    required_amount = db.Column(db.Integer, nullable=False)
    orders = db.relationship('Order', backref='donation', lazy=True)

    def __repr__(self):
        return f"<Donation(id={self.id}, name='{self.donation_name}', required_amount={self.required_amount})>"

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    donation_id = db.Column(db.Integer, db.ForeignKey('donations.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    donation_amount = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, donation_id={self.donation_id}, amount={self.donation_amount})>"
