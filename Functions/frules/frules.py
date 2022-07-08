from flask import Flask, jsonify, request
import requests
import sys
import json
import os

app= Flask(__name__)
@app.route("/", methods=["GET","POST"])
def postf():  
        url=os.environ['RULESCHK']

        response=requests.get(url)


        response = json.loads(response.text)
        rules={}
        rules['rules']=response

        url=os.environ['PADDING']
        response=requests.get(url)
        return jsonify(rules)

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')