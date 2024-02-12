from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.signinforms import UserLoginForm
from app.signupforms import UserSignUpForm
from app.models import User, db, check_password_hash
from flask_login import login_user, logout_user
from sqlalchemy.exc import SQLAlchemyError
import jwt
import os

auth = Blueprint('auth', __name__, template_folder='auth_templates')

def extract_email_from_token(token):
    # Your logic to extract user information from the token
    # For now, let's assume the token is a simple string, and we extract email directly
    return token

@auth.route('/signup', methods=['POST'])
def sign_up():
    try:
        data = request.get_json()
        token = data.get('token')

        print(f"Received token: {token}")

        user_email = extract_email_from_token(token)

        print(f"Extracted user email: {user_email}")
        
        existing_user = User.query.filter_by(email=user_email).first()
        if existing_user:
            return jsonify({'message': 'User already exists'}), 400

        # Create a new user based on token information
        new_user = User(email=user_email)
        db.session.add(new_user)
        db.session.commit()

        # Generates a token for Firebase Authentication
        payload = {"uid": str(new_user.id)}
        token = jwt.encode(payload, os.environ.get('44b5ece20e4ff45341d9b54d1c0fe3b30deca38f'), algorithm='HS256')

        return jsonify({'message': 'User created successfully', 'token': token}), 200

    except Exception as e:
        print(f"Error processing token: {e}")
        return jsonify({'message': 'Error processing token'}), 400

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = UserLoginForm()
    
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            
            logged_user = User.query.filter_by(email=email).first()
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