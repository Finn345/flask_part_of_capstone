from flask import Flask
from backend.config import Config
from .api.routes import api
from .site.routes import site
from .authentication.routes import auth

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.models import db, login_manager, ma
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from app.helpers import JSONEncoder

app = Flask(__name__)
CORS(app)

app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)

app.config.from_object(Config)

db.init_app(app)

migrate = Migrate(app, db)

login_manager.init_app(app)
login_manager.login_view = 'home'

ma.init_app(app)

app.json_encoder = JSONEncoder

CORS(app)
