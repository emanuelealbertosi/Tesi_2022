from flask import Flask, jsonify, request
import requests,json
import os


app= Flask(__name__)
@app.route("/", methods=["POST"])
def postf():
    if request.method=='POST':
        posted_data = request.get_json()
        url=os.environ['MYMAPS']

        payload={}
        payload['coordinate']=posted_data['coordinate']
        payload['type']="store"
        payload['radius']=100
        response=requests.post(url,json=payload)
        shops = json.loads(response.content)
        response={}
        for shop in shops['results']:
            response[shop['name']]=shop['vicinity']
        return jsonify(response)
       
        

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')