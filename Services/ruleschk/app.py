from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



def create_app():
    app = Flask(__name__)

    app.secret_key = 'xxxxxx'
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://xxxxxxxx"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

 
    db.init_app(app)
    
    return app