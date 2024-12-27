from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms import validators
# the folowing validators should be exactly in the way they are imported
# importing it as "from wtforms import validators.Email" is wrong and can bring to an error 
from wtforms.validators import DataRequired, Length, Email, EqualTo
from myapp.models import User

class RegisterForm(FlaskForm):
    username = StringField("username", validators=[DataRequired(), Length(min=2, max=10)])
    email = StringField("email", validators=[DataRequired(), Email()])

    password = PasswordField("password", validators=[DataRequired()])
    confirmPassword = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])

    submit = SubmitField("Sign Up")

    # Add custom validation
    # Use template method def validate_field(self, field):
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            print("Username exception")
            raise ValidationError("The username is already exists. Try another one")
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("The email is already exists. Try another one")
        

class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])

    rememberMe = BooleanField()
    submit = SubmitField("log in")