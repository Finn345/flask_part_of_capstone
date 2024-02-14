from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.signinforms import UserLoginForm
from app.signupforms import UserSignUpForm
from app.models import User, db, check_password_hash
from flask_login import login_user, logout_user
from sqlalchemy.exc import SQLAlchemyError
import uuid

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods=['POST'])
def sign_up():
    try:
        data = request.get_json()
        user_data = data.get('user')

        if not user_data:
            return jsonify({'error': 'No user data provided'}), 400

        user_email = user_data.get('email')
        user_password = user_data.get('password')
        user_first_name = user_data.get('firstName')
        user_last_name = user_data.get('lastName')

        if not user_email or not user_password or not user_first_name or not user_last_name:
            return jsonify({'error': 'Email, password, first name, and last name are required'}), 400

        existing_user = User.query.filter_by(email=user_email).first()
        if existing_user:
            return jsonify({'error': 'User already exists'}), 400

        new_user = User(
            id=str(uuid.uuid4()),
            email=user_email,
            password=check_password_hash(user_password),
            first_name=user_first_name,
            last_name=user_last_name
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User created successfully'}), 200

    except Exception as e:
        print(f"Error processing sign-up request: {e}")
        db.session.rollback()
        return jsonify({'error': 'An error occurred during sign-up'}), 500

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