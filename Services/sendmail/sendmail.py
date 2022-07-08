from flask import Flask, jsonify, request
import requests,json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import ssl, smtplib
from io import BytesIO
import base64


app= Flask(__name__)
@app.route("/", methods=["POST"])
def postf():

    posted_data = request.get_json()
    image=posted_data['image']
    print(image)
    recipient=posted_data['recipient']


    image=MIMEImage(base64.b64decode(image),_subtype='JPEG')
    image.add_header('Content-Disposition', 'attachment', filename='result.jpg')
    
    sender='xxxxxxxxxx'
    password = 'xxxxxxxxxx'
    msg_root = MIMEMultipart('alternative')
    msg_root['Subject'] = "AR application image"
    msg_root['From'] = sender
    msg_root['To'] = recipient

    msgAlternative = MIMEMultipart('alternative')
    msgAlternative.attach(MIMEText('<html><body>ARimage</body></html>', "html"))
    msg_root.attach(msgAlternative)
    msg_root.attach(image)
 
    text="<html><body>AR application image result</body></html>"

    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender, password) 
    text = msg_root.as_string()
    session.sendmail(sender, recipient, text)
    session.quit()
    print('Mail Sent')
    return "sent",200

        

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')