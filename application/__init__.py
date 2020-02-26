# import Flask class from the flask module
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
#import flask_bcrypt from bcrypt
from flask_bcrypt import Bcrypt
#import glask login library
from flask_login import LoginManager

# create a new instance of Flask and store it in app 
app = Flask(__name__)
#define the bcrypt
bcrypt = Bcrypt(app)


app.config['SQLALCHEMY_DATABASE_URI'] = str(os.getenv('DATABASE_URI'))
app.config['SECRET_KEY'] = str(os.getenv('SECRET_KEY'))
db = SQLAlchemy(app)
# import the ./application/routes.py file
login_manager = LoginManager(app)
login_manager.login_view="login"
from application import routes
