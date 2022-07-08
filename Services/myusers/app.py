from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL

db = SQLAlchemy()
mysql = MySQL()


def create_app():
    app = Flask(__name__)

    app.secret_key = 'xxxxxxx'
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql:/xxxxxxxxxxxx"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
 
    db.init_app(app)
    
    return app