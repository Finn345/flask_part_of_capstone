from flask_sqlalchemy import SQLAlchemy
import secrets
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False, default='')
    last_name = db.Column(db.String(150), nullable=False, default='')
    email = db.Column(db.String(150), nullable=False, unique=True, default='')
    password = db.Column(db.String(150), nullable=False, default='')
    g_auth_verify = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, unique=True, default='')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    projects = db.relationship('Project', backref='owner', lazy=True)

    def __init__(self, email, first_name='', last_name='', password='', g_auth_verify=False):
        self.id = secrets.token_hex(8)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = generate_password_hash(password)
        self.token = create_access_token(identity=str(self.id), expires_delta=False)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        token = create_access_token(identity=str(self.id), expires_delta=False)
        self.token = token
        return token

    def set_id(self):
        return secrets.token_hex(8)

    def set_password(self, password):
        self.password = generate_password_hash(password)
        return self.password

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"Welcome! {self.first_name} User {self.email} has been added to the database."

class Project(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(150), nullable=False, default='')
    description = db.Column(db.String, nullable=False, default='')
    language_to_use = db.Column(db.String(250), nullable=False, default='')
    amount_of_lines_to_use = db.Column(db.String(250), nullable=False, default='')
    is_it_a_webpage = db.Column(db.String(10), nullable=False, default='')
    user_token = db.Column(db.String, db.ForeignKey(User.token), nullable=False)

    def __init__(self, name, description, language_to_use, amount_of_lines_to_use, is_it_a_webpage, user_token, id=''):
        self.id = id if id else self.set_id()
        self.name = name
        self.description = description
        self.language_to_use = language_to_use
        self.amount_of_lines_to_use = amount_of_lines_to_use
        self.is_it_a_webpage = is_it_a_webpage
        self.user_token = user_token

    def __repr__(self):
        return f"The project {self.name} has been added"

    def set_id(self):
        return(secrets.token_urlsafe())

class ProjectSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'language_to_use', 'amount_of_lines_to_use', 'is_it_a_webpage']

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)
