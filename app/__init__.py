from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message


app = Flask(__name__)

app.config.from_object('app.config.Config')


db = SQLAlchemy(app) # flask-sqlalchemy
bc = Bcrypt(app) # flask-bcrypt

lm = LoginManager() # flask-loginmanager
lm.init_app(app)# init the login manager

mail = Mail(app)


from app import routes, models

with app.app_context():
    db.create_all()
