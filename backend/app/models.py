from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable=True, default='')
    email = db.Column(db.String(150), nullable=False, unique=True, default='')
    password = db.Column(db.String(150), nullable=False, default='')
    g_auth_verify = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, unique=True, default='')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    project = db.relationship('Project', backref='owner', lazy=True)
    
    def __init__(self, email, first_name='', last_name='', id='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.token = self.set_token(10)
        self.g_auth_verify = g_auth_verify
        
    def set_token(self, length):
        return secrets.token_hex(length)
    
    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def _repr__(self):
        return f"Welcome! {self.first_name} User {self.email} has been added to the database."
    
import secrets
from app.models import db, ma, User

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
        return f"The project {self.name} has been added, thanks!"

    def set_id(self):
        return secrets.token_urlsafe()

class ProjectSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'language_to_use', 'amount_of_lines_to_use', 'is_it_a_webpage']

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)
