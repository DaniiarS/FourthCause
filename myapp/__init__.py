from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'aa3cd44177763f2ec3d646d88b89629c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# Specify the login route
# LoginManager's login_view attribute specifies the route to the login page whenever a user tries to get access to the pages where the route has login_required decorator
login_manager.login_view = 'login'

print("myapp module is executed")

from myapp import routes
