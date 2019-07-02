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
import json
import sys

PORT = 8000

#https://stackoverflow.com/questions/39801718/how-to-run-a-http-server-which-serve-a-specific-path
#the following changes the defalut directory copied from the reference aboth
web_dir = os.path.join(os.path.dirname(__file__), 'http')
os.chdir(web_dir)

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    
    def getdata(self):
        length = int(self.headers['Content-Length'])
        bindata=self.rfile.read(length)
        data=str(bindata,encoding='utf8')
        
        return data
    
    def senddata(self, data):
        self.send_response(200)
        #self.send_header("Method FINDUSER","send")
        self.end_headers
        self.wfile.write(data)
        
        return data    
    
    def do_POST(self):
        #Find a function which buffers the incomming data
        #Add a json function to add a new message to the requestet file
        #Maybe have a look here
        #https://stackoverflow.com/questions/33662842/simple-python-server-to-process-get-and-post-requests-with-json
        #https://stackoverflow.com/questions/17690585/how-do-i-access-the-data-sent-to-my-server-using-basehttprequesthandler
        data=self.getdata()
        pydict=json.loads(data)
        
        publickeys=pydict["publickeys"]
        message=pydict["message"]
        sender=pydict["senderID"]
        UserID_bob=pydict["receiverID"]
        keyID_alice= pydict['keyID_alice']
        keyID_bob= pydict['keyID_bob']
        method=pydict['method']
        nowtimedate=pydict['nowtimedate']
        #get data from sender
        file=open(sender +'.json', 'r')
        extndData=json.load(file)
        
        #update the server dicitionary
        extndData["message"][UserID_bob].update({nowtimedate: {"keyID": keyID_bob , "message": message }})
        extndData["mykey"].update({  "keyID" : keyID_alice, "method" : method ,"publickey": publickeys})
        #write the server dicitonary
        filepath= sender+".json"
        outfile=open(filepath, 'w')
        json.dump(extndData,outfile)
        
    def do_POSTKEY(self):
        data=self.getdata()
        pydict=json.loads(data)
        publickeys=pydict["publickeys"]
        keyID_alice= pydict['keyID_alice']
        method=pydict['method']
        sender=pydict["senderID"]
        
        file=open(sender +'.json', 'r')
        extndData=json.load(file)
        
        extndData["mykey"].update({  "keyID" : keyID_alice, "method" : method ,"publickey": publickeys})
        
        filepath= sender+".json"
        outfile=open(filepath, 'w')
        json.dump(extndData,outfile)
    
    def do_FINDUSER(self):
        data=self.getdata()
        pydict=json.loads(data)
        sender=pydict["UserID"]
        filepath= sender+".json"
        boolval=os.path.isfile(filepath)
        
        jsond=json.dumps({"exists":boolval})
        data=bytes(jsond,encoding='utf8')
        self.senddata(data)
        
    def do_CREATEACCOUNT(self):
        data=self.getdata()
        pydict=json.loads(data)
        UserID_bob=pydict["UserID_bob"]
        
        filepath= UserID_bob +".json"
        boolval=os.path.isfile(filepath)
        
        #I am afraid of, that the http server doesn't handle requests chronologically
        #but instead parallel, so the following then could create an error:
        #Say "A" likes to create an account and asks the server if the account
        #does already exist. 
        #If tbe server allows for parallel procession, someone "B" could in the meantime
        #do the same request and cause potential errors for "A" if he can create the account 
        #faster than "A".
            
        dict_py={"UserID" :UserID_bob,
                    "message" : {
                            UserID_bob: {
                                    "28.05.2019":{
                                            "keyID": "1",
                                            "message": ""
                                            }
                                    }
                                    },
                    "mykey" : {  "keyID" : 1,
                               "method" : "rsa",
                               "publickey": "123423"
                               }
                    }
        
        
        if boolval!=True:
            outfile=open(filepath, 'w')
            json.dump(dict_py,outfile)
            
        #send back 
        jsond=json.dumps({"exists":boolval})
        data=bytes(jsond,encoding='utf8')
        self.senddata(data)
        
    def do_ADDCONTACT(self):
        data=self.getdata()
        pydict=json.loads(data)
        UserID_bob=pydict["UserID_bob"]
        UserID_alice=pydict["UserID_alice"]
        filepath=UserID_alice +'.json'
        file=open(filepath, 'r')
        extndData=json.load(file)
        file.close()
        extndData["message"].update({ UserID_bob: {
                                    "28.05.2019":{
                                            "keyID": "1",
                                            "message": ""
                                            }
                                    }})
        outfile=open(filepath, 'w')
        json.dump(extndData,outfile)
        outfile.close()
        
        boolval=os.path.isfile(UserID_bob +'.json')
        jsond=json.dumps({"exists":boolval})
        data=bytes(jsond,encoding='utf8')
        self.senddata(data)
        
    def do_GETMESSAGES(self):
        data=self.getdata()
        pydict=json.loads(data)
        nowtimedate=pydict["timedate"]
        UserID_bob=pydict["UserID_bob"]
        UserID_alice=pydict["UserID_alice"]
        
        file=open(UserID_bob +'.json', 'r')
        serverData=json.load(file)
        keyset=set(serverData["message"][UserID_alice].keys())
        #filter keys with border given by request
        keys_trunc=[x for x in keyset if x > nowtimedate]
        keys_trunc.sort()
        message_trunc=[]
        for i in range(len(keys_trunc)):
            message_trunc.append([keys_trunc[i],serverData["message"][UserID_alice][keys_trunc[i]]])
        pydict={"messages":message_trunc}
        jsondict=json.dumps(pydict)
        data=bytes(jsondict,encoding='utf8')
        self.senddata(data)
        
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