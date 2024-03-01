#-----/Imports need/-----
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
# import MySQLdb.cursors

# from flask_mail import Mail
import os
# from ..app.email import send_email
#-----/Imports app configuration/-----
from config.config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
mysql = MySQL()
# mail = Mail()


#-----/This is so important for the login/-----
login_manager = LoginManager()
#-----/This is when page requires access redirects to the path/-----
login_manager.login_view = 'auth.login'


def create_app(config_name):

    app = Flask(__name__)#-----/Get the place the app is defined/-----
    app.config.from_object(config[config_name])#-----/This is a function to load the catual configuration/-----
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')

    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    

   
    # app.config['MYSQL_HOST'] = 'localhost'
    # app.config['MYSQL_USER'] = 'root'
    # app.config['MYSQL_PASSWORD'] = 'luiscarlos2004'
    # app.config['MYSQL_DB'] = 'projectChurch'
    
    
    db.init_app(app)
    mysql.init_app(app)
    # mail = Mail(app)
    
    #Routes of blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
        
    login_manager.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    return app

# send_email()

