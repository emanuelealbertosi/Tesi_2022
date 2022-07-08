from flask import Flask, jsonify, request
# initialize our Flask application
app= Flask(__name__)
import base64
import io
import time
import os
import googlemaps
from datetime import datetime



    

@app.route("/", methods=["POST"])
def postf():
    posted_data = request.get_json()
    gmaps = googlemaps.Client(key=os.environ['API_KEY'])
    
    

    location = posted_data['coordinate']
    type = posted_data['type']

    radius = posted_data['radius']

    result=gmaps.places_nearby(
            location=location,
            radius=radius,

            open_now=True,
            type=type,
            
        )

    return jsonify(result)

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')