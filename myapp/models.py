from myapp import db
from myapp import login_manager
from flask_login import UserMixin

# the decarator below tells the flask_login to use the function below any time it needs to retreive a user from the database. Flask stores user_id only in its cookies in the session, therefore it uses user_id to retreive the object from the database.
@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

# UserMixin - provides implentations that flask_login expects a user object to have
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

    image = db.Column(db.String(16), nullable=False, default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User({self.username}, {self.email})"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post({self.title})"