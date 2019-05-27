#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 19:28:05 2019

@author: stephan
"""

##my home adress currently is 188.22.60.96.
#but its dynamic so might change
#I forwarded the port 8000, so thus 
#i could acess my filsystem on the raspbery pi with
#http://188.22.60.96:8000/

#I added the following line
#@/usr/bin/python3 /home/pi/http/server.py
#to the file acessed by
#sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
# so in order to make it startup at boot
#see also:
#https://www.raspberrypi-spy.co.uk/2014/05/how-to-autostart-apps-in-rasbian-lxde-desktop/

import http.server
import socketserver
import os

PORT = 8000

#https://stackoverflow.com/questions/39801718/how-to-run-a-http-server-which-serve-a-specific-path
#the following changes the defalut directory copied from the reference aboth
web_dir = os.path.join(os.path.dirname(__file__), 'http')
os.chdir(web_dir)

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        ...
        #Find a function which buffers the incomming data
        #Add a json function to add a new message to the requestet file
        #Maybe have a look here
        #https://stackoverflow.com/questions/33662842/simple-python-server-to-process-get-and-post-requests-with-json
        #https://stackoverflow.com/questions/17690585/how-do-i-access-the-data-sent-to-my-server-using-basehttprequesthandler
        length = int(self.headers['Content-Length'])
        bindata=self.rfile.read(length)
        data=str(bindata,encoding='utf8')
        print(data)
Handler =  MyHTTPRequestHandler

#the following code is copied from refernce
#https://docs.python.org/3.7/library/http.server.html
#just that i defined http instead of making an with statment
#as the code didn't work with the with statment on my raspberry

httpd=socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()

#For zechnical background read:
#https://github.com/python/cpython/blob/3.7/Lib/http/server.py
#https://docs.python.org/3.7/library/socketserver.html
#so in order to understand why defining a "Hanlder" -class