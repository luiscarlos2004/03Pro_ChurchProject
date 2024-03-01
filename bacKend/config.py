#-----/Importing some modules/-----

import os
from dotenv import load_dotenv


#-----/Creating the pathname/-----

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv('.env')

#-----/Starts class config/-----

class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY')
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'luiscarlosvaldivieso3@gmail.com'
    MAIL_PASSWORD = 'uzou scpw siem cjph'

    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'luiscarlos2004'
    MYSQL_DB = 'projectChurch'

    #-----/This not required a class intance creation/-----
   
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,os.environ.get('DEV_DATABASE_URL'))
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:luiscarlos2004@localhost/church'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,os.environ.get('TEST_DATABASE_URL'))
 
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,os.environ.get('DATABASE_URL'))

config={

    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,
    'default':DevelopmentConfig

}