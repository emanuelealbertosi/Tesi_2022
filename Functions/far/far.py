from flask import Flask, jsonify, request,send_file
import asyncio
import aiohttp 
import requests
import sys
import json
import smtplib, ssl
from PIL import Image, ImageDraw,ImageFont
from io import BytesIO
import base64
import os


app= Flask(__name__)

async def fetch_url(session, url, payload):
    
    async with session.post(url,json=payload) as response:
        return await response.text()

@app.route("/", methods=["POST"])
async def postf():
    if request.method=='POST':
        posted_data = request.get_json()
        userinfo = posted_data['userinfo']
        dcc=posted_data['dcc']
        id=posted_data['id']
        coordinate=posted_data['coordinate']
        image=posted_data['image']

        payload_fcrop={'id':id,'image':image,'coordinate':coordinate}
        payload_fdcc={'id':id,'userinfo':userinfo,'dcc':dcc,'coordinate':coordinate}
        fcrop_url=os.environ['FCROP']  
        fdcc_url=os.environ['FDCC']
       
        async with aiohttp.ClientSession() as session:
            tasks = []
            task = asyncio.create_task(fetch_url(session, fcrop_url ,payload_fcrop))
            tasks.append(task)
            task = asyncio.create_task(fetch_url(session, fdcc_url ,payload_fdcc))
            tasks.append(task)
            sites = await asyncio.gather(*tasks)
        shops = json.loads(sites[0]) 
        advise=json.loads(sites[1]) 
        image = Image.open(BytesIO(base64.b64decode(image))) 
        draw=ImageDraw.Draw(image)
        print(advise)
        print(shops)
        print(shops['shop_status'][0]['Name'])
        shop_status="Negozio:"+ shops['shop_status'][0]['Name']
        
        fontsize=11
        fnt = ImageFont.truetype("Roboto-Black.ttf",fontsize)
        leftborder=7
        topmargin=1
        if (shops['shop_status'][0]['Name']=="aperto"):
            draw.text((leftborder+1,topmargin),shop_status,font=fnt,fill=(153,255,153))
        else:  
            draw.text((leftborder,topmargin),shop_status,font=fnt,fill=(255,51,51))  
        topmargin=15    
        draw.text((leftborder,topmargin),"Negozi aperti nelle vicinanze:",font=fnt,fill=(153,255,153))
        topmargin=19
        for name,addr in  shops['shops_nearby'].items():
            print (name+" "+addr)
            topmargin+=10
            draw.text((leftborder+4,topmargin),name+":  "+addr,font=fnt,fill=(255,255,102))
        topmargin=200
        if 'regulation' in advise:
            draw.text((leftborder,topmargin),"Regolamento con GP valido:",font=fnt,fill=(153,255,153))
            for id,regulation in  advise['regulation'].items():
                print (id+": "+regulation)
                topmargin+=10
                draw.text((leftborder+4,topmargin),id+":  "+regulation,font=fnt,fill=(0,0,0))
        else:
            draw.text((leftborder,topmargin),"Regolamento senza GP valido:",font=fnt,fill=(255,51,51))  
            for id,rule in  advise['rules'].items():
                print (id+": "+rule)
                topmargin+=10
                draw.text((leftborder+4,topmargin),id+":  "+rule,font=fnt,fill=(0,0,0))  
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        image_str=base64.b64encode(buffered.getvalue()).decode("ascii")
        print(image_str)

        url=os.environ['SENDMAIL']
        payload={}
        payload['recipient']=userinfo
        payload['image']=image_str
        requests.post(url,json=payload)
        
        return jsonify({"image":image_str})

        
if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')