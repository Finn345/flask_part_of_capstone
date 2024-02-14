from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.signinforms import UserLoginForm
from app.signupforms import UserSignUpForm
from app.models import User, db, check_password_hash, generate_password_hash
from flask_login import login_user, logout_user
from sqlalchemy.exc import SQLAlchemyError
import uuid4
import re

auth = Blueprint('api', __name__, template_folder='auth_templates')

from flask import Flask, request, jsonify
from models import User, db

app = Flask(__name__)

@auth.route('/user', methods=['POST'])
def signup():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data or 'firstName' not in data or 'lastName' not in data:
        return jsonify({'error': 'All fields are required.'}), 400
    if not re.match(r'^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}$', data['email']):
        return jsonify({'error': 'Please enter a valid email address.'}), 400
    if len(data['password']) < 8:
        return jsonify({'error': 'Password must be at least 8 characters long.'}), 400
    user = User(id=str(uuid4()), email=data['email'], password=generate_password_hash(data['password']), firstName=data['firstName'], lastName=data['lastName'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully.'}), 201

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            user_email = form.email.data
            user_password = form.password.data

            user = User.query.filter_by(email=user_email).first()
            if user and check_password_hash(user.password, user_password):
                login_user(user)
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