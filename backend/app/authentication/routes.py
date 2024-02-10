from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import User, db, check_password_hash
from app.signupforms import UserSignUpForm
from app.signinforms import UserLoginForm

from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    form = UserSignUpForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            first_name = form.first_name.data
            last_name = form.last_name.data

            existing_user = User.query.filter_by(email=email).first()

            if existing_user:
                flash('Email already registered. Please use a different email or log in.', 'user-exists')
                return redirect(url_for('auth.sign_up'))

            user = User(email=email, password=password, first_name=first_name, last_name=last_name)
            db.session.add(user)
            db.session.commit()

            flash(f'Account created successfully for {email}. Welcome!', 'user-created')
            return redirect(url_for('site.home'))
    except:
        raise Exception('Invalid data has been entered: Please check the data entered')
    
    return render_template('signup.html', form=form)

from sqlalchemy.exc import SQLAlchemyError

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = UserLoginForm()
    
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            
            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('Welcome', 'auth-success')
                return redirect(url_for('site.home'))
            else:
                flash('Login attempt failed; Please check your information', 'auth-failed')
                return redirect(url_for('auth.signin'))
    except SQLAlchemyError as e:
        print(f"SQLAlchemyError: {e}")
        flash('An error has occured trying to sign in/sign up. Please try again later.', 'auth-error')
    return render_template('signin.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))