from pickle import TRUE
from flask import Flask, jsonify, request
import sys
# initialize our Flask application
#app= Flask(__name__)
from app import create_app,db
from models import Dcc

app = create_app()
@app.route("/", methods=["GET","POST"])
def postf():
        
        regulations = Dcc.query.filter_by(isvalid=True).all()
        regulation_dict={}
        for regulation in regulations:
            regulation_dict[regulation.id]=regulation.regulation   
        return jsonify(regulation_dict)    

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')