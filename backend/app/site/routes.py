from flask import Blueprint, render_template
from app.models import Project
from flask_login import current_user

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    projects = Project.query.all()
    user_first_name = current_user.first_name if current_user.is_authenticated else None
    return render_template('index.html', projects=projects, user_first_name=user_first_name)

@site.route('/profile')
def profile():
    return render_template('profile.html')

@site.route('/about')
def about():
    return render_template('about.html')