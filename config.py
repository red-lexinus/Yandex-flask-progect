from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager
import os
import tokens

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{tokens.USERNAME}:{tokens.PASSWORD}@{tokens.HOST}/{tokens.BASE_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = tokens.SECRET_KEY
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'youmail@gmail.com'
app.config['MAIL_DEFAULT_SENDER'] = 'youmail@gmail.com'
app.config['MAIL_PASSWORD'] = 'password'
app.config['SUM'] = 0
app.config['APP_DIR'] = os.path.abspath(os.path.dirname(__file__))
app.config['STATIC_DIR'] = os.path.join(app.config['APP_DIR'], 'static')
app.config['UPLOAD_DIR'] = os.path.join(app.config['STATIC_DIR'], 'img')

db = SQLAlchemy(app)

#login_manager = LoginManager(app)
#login_manager.login_view = 'login'


