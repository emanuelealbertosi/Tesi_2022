from flask import Flask, jsonify, request
import requests,json
import os


app= Flask(__name__)
@app.route("/", methods=["POST"])
def postf():
        posted_data = request.get_json()
        url=os.environ['MYCROP']
        
        response=requests.post(url,json=posted_data,timeout=1200)
        shop_status = json.loads(response.text)

        url=os.environ['FGEO']
        response=requests.post(url,json=posted_data)
        shops_nearby = json.loads(response.text)
  
        response={}
        response['shop_status']=shop_status

        response['shops_nearby']=shops_nearby
         
        return jsonify(response)
        

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')