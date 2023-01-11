from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hasiodhas hiduaysudywqbe'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URI"]

db = SQLAlchemy(app)
db.init_app(app)

from .models import Ideas

with app.app_context():
    db.create_all()
    db.session.commit()

from website.views import views

app.register_blueprint(views, url_prefix='/')
