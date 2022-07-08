from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_mysqldb import MySQL

db = SQLAlchemy()
#mysql = MySQL()


def create_app():
    app = Flask(__name__)

    app.secret_key = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://app:ubuntu@192.168.1.120/rules"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    #app.config['MYSQL_HOST'] = '192.168.1.120'
    #app.config['MYSQL_USER'] = 'app'
    #app.config['MYSQL_PASSWORD'] = 'Ubuntu123!'
    #app.config['MYSQL_DB'] = 'dcc'
 
    db.init_app(app)
    
    return app