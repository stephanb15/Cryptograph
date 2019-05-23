#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 20:34:56 2019

@author: stephan
"""
from requests import get

import subprocess
import sys
import json
import time

#(i)This applications task is nothing more than geting my local ip adress and
#sending it to the uni wien webserver

#(ii)
#I added the following line
# @/usr/bin/python3 /home/pi/sendip.py
#to the file acessed by
#sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
# so in order to make it startup at boot
#see also:
#https://www.raspberrypi-spy.co.uk/2014/05/how-to-autostart-apps-in-rasbian-lxde-desktop/



def getip():
    #mostly coppied from
    #https://stackoverflow.com/questions/2311510/getting-a-machines-external-ip-address-with-python/41432835
    #get the ip from some website earning a necessary tool- unsave as dependenc (website) can dissapear
    ip = get('https://api.ipify.org').text
    return ip
    
def send(myip):
    #this funtion sends the ip adress to the dedicated file on the uni webserver
    #https://data-flair.training/blogs/python-subprocess-module/
    #https://gist.github.com/bortzmeyer/1284249
    #write an if condition - if directory media/pers/html  does not exists, do:
    #cmd="stephanb15@login.univie.ac.at:./ /media/pers -o allow_other"
    
    #subprocess.run(["sshfs", cmd])
    
    #subprocess.run(["cd", "media/pers/html/Appliactions/Cryptograph"])
    
    data = {
            "ip": myip
            }
    
    destination="/media/pers/fileserver/html/Applications/Cryptograph/serverip.json"
    with open(destination, "w") as f:
        json.dump(data,f)
    
print(getip())

myip="123456789"
#a random initial value

while True:
    time.sleep(5)
    newip=getip()
    if myip != newip:
        myip=newip
        send(myip)
        
        
    