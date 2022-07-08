from flask import Flask, jsonify, request
import requests
import sys
import json
import os

app= Flask(__name__)
@app.route("/", methods=["GET","POST"])
def postf():
        
        url=os.environ['DCCCHK']
        response=requests.get(url)
        response = json.loads(response.text)
        regulation={}
        regulation['regulation']=response
        return jsonify(regulation)

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')