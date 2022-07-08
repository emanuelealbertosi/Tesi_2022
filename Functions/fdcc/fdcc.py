from flask import Flask, jsonify, request
import requests
import sys
import json
import os

app= Flask(__name__)
@app.route("/", methods=["POST"])
def postf():
    if request.method=='POST':
        posted_data = request.get_json()
        username = posted_data['userinfo']
        dcc=posted_data['dcc']
        request_dict={'username':username,'dcc':dcc}
        
        url=os.environ['GREENPASSAPI']
    
        response=requests.post(url,json=request_dict)
        if response.status_code!=200:
            isvalid=False
        else:    
            response = json.loads(response.text)
            isvalid=response   
        if isvalid:
            url=os.environ['FUNT']

            response=requests.get(url)
            response = json.loads(response.text)
            return jsonify(response)
        else:
            url=os.environ['FUNF']

            response=requests.get(url)

            response = json.loads(response.text)
            return jsonify(response)

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')