from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Donations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(10000))
    project_amount = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    donations = db.relationship('Donations')

