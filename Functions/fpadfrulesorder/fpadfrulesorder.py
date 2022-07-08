from flask import Flask, jsonify, request
import requests,json
import os


app= Flask(__name__)
@app.route("/", methods=["GET","POST"])
def postf():
    
    url="http://192.168.1.106:5000"
    requests.get(url)
    return 200
        

       
        

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')