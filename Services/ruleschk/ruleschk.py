from pickle import TRUE
from flask import Flask, jsonify, request
import sys
import json

from app import create_app,db
from models import Rules

app = create_app()
@app.route("/", methods=["GET","POST"])
def getf():

    rules = Rules.query.filter_by(isvalid=True).all()
    
    rules_dict={}
    for rule in rules:
        rules_dict[rule.id]=rule.rule
    
    return jsonify(rules_dict)
          
if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')