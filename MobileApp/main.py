# import all the relevant classes
from urllib import request
from kivy.app import App
import requests
import certifi
import json
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty,StringProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import mainthread
from kivy.utils import platform
from kivy.network.urlrequest import UrlRequest
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import urllib

import base64
from PIL import Image,ImageChops
import time
import os
from io import BytesIO

USERNAME=''
PASSWORD=''  

class PopupWindow(Widget):
    def btn(self):
        popFun()
  
# class to build GUI for a popup window
class P(FloatLayout):
    pass
  
# function that displays the content
def popFun(image):
    show = P()
    window = Popup(title = "popup", content = Image.open(image),
                   size_hint = (None, None), size = (300, 300))
    window.open()
  
# class to accept user info and validate it
class loginWindow(Screen):
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)
    def validate(self):
         # switching the current screen to display validation result
            
            print(self.email.text)
            print(self.pwd.text)
            os.environ['USERNAME']=self.email.text
            os.environ['PWD']=self.pwd.text
            sm.current = 'camerac'
  
            # reset TextInput widget
            #self.email.text = ""
            #self.pwd.text = ""
  
  

      
# class to display validation result
class CameraClick(Screen):
    def capture(self): 
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        email = ObjectProperty(None)
        pwd = ObjectProperty(None)
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        path=camera.export_to_png("IMG_{}.png".format(timestr))
        print(path)
        
        img = Image.open("IMG_{}.png".format(timestr))
        
        img = self.autocrop(img)
        im_file = BytesIO()
        img.save(im_file, format="PNG")
        #popFun(img)
        im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
        im_b64 = base64.b64encode(im_bytes)


  
        os.remove("IMG_{}.png".format(timestr))
   


        username=os.environ['USERNAME']
        password=os.environ['PWD']
        image=str(im_b64.decode('utf8'))
        
        coordinate=requests.post("https://www.googleapis.com/geolocation/v1/geolocate?key=XXXXXXXXXXXXXXXXXXXXXXX")
        result=json.loads(coordinate.text)
        print(result)
        coordinate=str(result['location']['lat'])+", "+ str(result['location']['lng'])
      
        print(coordinate)
        params = json.dumps({'username':username,'password':password,'image':image,'coordinate':coordinate})
        
        
        headers = {'Content-type': 'application/json',
                  'Accept': '*/*'}
        req = UrlRequest('https://xxxxxxxx.', on_success=self.AR_result,on_failure=self.AR_failure,req_body=params,req_headers=headers)         

    def AR_result(self,req, result):

        result=json.loads(result)
        

        im_bytes = base64.b64decode(result['image'])   # im_bytes is a binary image
        im_file = BytesIO(im_bytes)  # convert image to file-like object
        img = Image.open(im_file)
       
        img.show()
        sm.current = 'camerac'

    def AR_failure(self,req, result):
        print('Failure')
        print('Failure')  
        print(result)  
    def AR_error(self,req, result):
        print('Error') 
        print('Failure')
        print(result)     

    def autocrop(self,im):
        bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
        diff = ImageChops.difference(im, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            return im.crop(bbox)

class windowManager(ScreenManager):
    pass
  
# kv file
kv = Builder.load_file('login.kv')
sm = windowManager()

if 'EMAIL' in os.environ:
    sm.add_widget(CameraClick(name='camerac'))
else:
    sm.add_widget(loginWindow(name='login'))
    sm.add_widget(CameraClick(name='camerac'))

  

class loginMain(App):
    def build(self):
        return sm
  

loginMain().run()