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
        username = posted_data['username']
        password=posted_data['password']
        coordinate=posted_data['coordinate']
        image=posted_data['image']
        request_dict={'username':username,'password':password}


        
        url=os.environ['MYUSERS']
 
        response=requests.post(url,json=request_dict)

        if response.status_code!=200:
            return 400
        else:  
            
            url=os.environ['FAR']
  
            response = json.loads(response.text) 
            request_dict={'id':response["id"],'userinfo':response["userinfo"],'dcc':response["dcc"],'coordinate':coordinate,'image':image}
 
            response = requests.post(url,json=request_dict)
 
            return response.content,200
   

if __name__=='__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'),debug=True,host='0.0.0.0')