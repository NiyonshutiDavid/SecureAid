from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///secureaid.db"  # Use secureaid.db for the database
app.config['SECRET_KEY'] = 'your_secret_key'  # Set a secret key for session management

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from SecureAid_app import routes  # Import routes after initializing app and db
