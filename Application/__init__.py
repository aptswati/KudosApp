from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine

app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)

db = MongoEngine()
db.init_app(app)

from Application import routes

