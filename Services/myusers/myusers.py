from flask import Flask, jsonify, request
import sys
# initialize our Flask application
#app= Flask(__name__)
from app import create_app,db
from models import User

app = create_app()
@app.route("/", methods=["POST"])
def postf():
    if request.method=='POST':
        posted_data = request.get_json()
        username = posted_data['username']
        password = posted_data['password']
        print(username,file=sys.stderr)
        user = User.query.filter_by(username=username).first()
        if user.password==password: 
            return jsonify({'id':user.id,'userinfo':user.username,'dcc':user.dcc})
        else:
            return 'error',400    
if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')