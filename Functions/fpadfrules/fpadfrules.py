from flask import Flask, jsonify, request
import requests,json
import os


app= Flask(__name__)
@app.route("/", methods=["GET","POST"])
def postf():
    
    url="http://192.168.1.106:5000"
    requests.get(url)
    url=os.environ['LINK']    
    if request.method=='POST': 

        response=requests.post(url)               
        response = json.loads(response.text)
        return jsonify(response)
    else:

        response=requests.get(url)
        response = json.loads(response.text)
        return jsonify(response)
        

       
        

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')