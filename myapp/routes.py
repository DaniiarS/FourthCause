from myapp import app, db, bcrypt
from flask import render_template, url_for, request, redirect, flash, abort
from myapp.forms import RegisterForm, LoginForm
from myapp.models import User
from flask_login import login_user, logout_user, current_user, login_required

# For my testing database
import json
import csv

database = {}

print("Route module is executed")


@app.route('/')
def home():
    return render_template('home.html')

# When the request method is POST, the newly created RegisterFomr() instance get automatically populated with data
# written by the requester
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:   
        return redirect(url_for('home'))
    

    form = RegisterForm()
    if form.validate_on_submit():
        
        # Adds a new user
        # It is important to execute app.app_context() to database to work
        # Use "with" statement because the app.app_context() should be handled properly and closed
        with app.app_context():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username = form.username.data, email=form.email.data, password = hashed_password)
            db.session.add(user)
            db.session.commit()
            
            flash(f'Account is created for {form.username.data}', 'success')
            return redirect(url_for("login"))

    return render_template('register.html', title="Register", form=form)



@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # You can also add remember=form.remember.data to enable "remember me" functionality
            # This is the moment the user is authenticated
            login_user(user)

            next_page = request.args.get('next') # the args here is the dictionary. We use get() method so that if the parameter is absent, the get() method returns None and does not throw an error
            if next_page:
                return redirect(next_page)
            
            return redirect(url_for('home'))
        else:
            print('Unsuccessful attempt to log in. Check email and passwrod.', 'danger')
    return render_template('login.html', title="Login", form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))



@app.route('/account')
@login_required # this decorator will require a user to be Loged In, to continue accessing the page. Therfore, it should redirect the anonymous user to log in page. To make the redirect work we have to set login_manager.login_view = 'function_name' in __init__.py
def account():
    return render_template('account.html', title="Account")


@app.route('/about')
def about():
    return render_template('about.html')

def import_data(file_name, database):
    # if file_name in database.keys():
    #     return database[file_name]
    
    try:
        with open(f'myapp/database/{file_name}.csv', 'r') as file:
            reader = csv.reader(file)
            database[file_name] = []
            for line in reader:
                if line[3] == 'eng':
                    line[3] = 'English'
                elif line[3] == 'rus':
                    line[3] = 'Russian'
                print(file_name, line[1])
                database[file_name].append(
                    {
                        'title': line[0],
                        'image': f'static/images/{file_name}/{line[1]}',
                        'description': line[2],
                        'language': line[3],
                        'source': line[4],
                        'link': line[5],
                        'type': line[6],
                    }
                )
    except:
        raise ReferenceError

    return database[file_name]


@app.route('/<path>')
def render_page(path):
    try:
        return render_template(f'{path}.html', database=import_data(path, database), path=path)
    except FileNotFoundError:
        abort(404)  # Return a 404 error for missing files
    except Exception as e:
        app.logger.error(f"Error processing request for {path}: {e}")
        abort(500)  # Return a generic 500 error for unexpected issues
    return render_template(f'{path}.html', database=import_data(path, database), path=path)