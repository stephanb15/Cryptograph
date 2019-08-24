#!/usr/bin/python3
#This file is created by author: Stephan Bornberg

import tkinter as tk
import json
import urllib.request
import requests
import os
import math
import datetime
import http.client
import traceback

from lib.RSA import RSA
from lib.transposition import Transposition
from lib.substitution import Substitution

##############################################################################
#                             Local FIles
##############################################################################

def FileExtractIP():
    wrkdir = os.path.dirname(__file__)
    path_IP_adress=os.path.join(wrkdir,"ipadress")
    get=open(path_IP_adress, 'r')
    ipstring=get.read()
    return ipstring.strip()

class USRdata():
    #This is a class handling user Data
    #like decrypted Messages etc
    wrkdir = os.path.dirname(__file__)
    
    dir_bob=lambda UserID_alice, UserID_bob, file : os.path.join(USRdata.wrkdir,"usr",UserID_alice, UserID_bob, file)
    dir_alice=lambda UserID_alice, file : os.path.join(USRdata.wrkdir,"usr",UserID_alice, file)
    
    def mkdir(path):
        #https://thispointer.com/how-to-create-a-directory-in-python/
        if not os.path.exists(path):
            os.mkdir(path)
    
    def mfile(path,message):
        if not os.path.isfile(path):
            write=open(path, 'w')
            write.write(message)
            write.close()
    
    def createFilestru_prim(UserID_alice):
        path_alice=os.path.join(USRdata.wrkdir,"usr",UserID_alice)
        USRdata.mkdir(path_alice)
        
        path_bob_key=USRdata.dir_alice(UserID_alice,"key.txt")
        open(path_bob_key, 'a').close()
        
    
    def createFilestru(UserID_alice, UserID_bob):
        
        #directories
        USRdata.createFilestru_prim(UserID_alice)
        path_bob=os.path.join(USRdata.wrkdir,"usr",UserID_alice, UserID_bob)
        USRdata.mkdir(path_bob)
        
        #files in directories
        path_bob_mes=USRdata.dir_bob(UserID_alice,UserID_bob,"messages.txt")
        USRdata.mfile(path_bob_mes,"1999-07-03 1"+" "+"Cryptograph"+">> "+"-Welcome to Cryptograph-"+'\n')
        
        path_bob_time=USRdata.dir_bob(UserID_alice,UserID_bob,"lastTime.txt")
        USRdata.mfile(path_bob_time,"1999-07-03")
        
    def store_Message(UserID_alice,UserID_bob,message,datetime):
        #messages must be an array of strings of format:
        #str(datetime.datetime.now())+" "+message
        USRdata.createFilestru(UserID_alice,UserID_bob)
        
        path_bob=USRdata.dir_bob(UserID_alice, UserID_bob,"messages.txt")
        write=open(path_bob, 'a')
        write.write(datetime+" "+message)
        write.close()
    
    def store_lastTime(UserID_alice,UserID_bob,datetime):
        #so in order to now the last recwived Message-Time of Bob
        path_bob=USRdata.dir_bob(UserID_alice, UserID_bob,"lastTime.txt")
        write=open(path_bob, 'w')
        write.write(datetime)
        write.close()
        
    def extract_lastTime(UserID_alice,UserID_bob):
        path_bob=USRdata.dir_bob(UserID_alice, UserID_bob,"lastTime.txt")
        read=open(path_bob, 'r')
        lastTime=read.readlines()[0]
        read.close()
        return lastTime
        
    def extract_allMessage(UserID_alice,UserID_bob):
        path_bob=USRdata.dir_bob(UserID_alice, UserID_bob,"messages.txt")
        read=open(path_bob, 'r')
        buffer=read.readlines()
        buffer2=[]
        for i in range(len(buffer)):
            linelist=buffer[i].split(" ",2)
            if len(linelist)==3:
                linelist2=[linelist[0]+linelist[1],linelist[2]+"\n"]
                buffer2.append(linelist2)
        read.close()
        
        return buffer2
    
    def store_keys(UserID_alice,keyID,method,key):
        path_alice=USRdata.dir_alice(UserID_alice,"key.txt")
        write=open(path_alice, 'a')
        write.write(keyID+" "+method +" "+key+"\n")
        write.close()
    
    def extract_keys(UserID_alice):
        USRdata.createFilestru_prim(UserID_alice)
        path_alice=USRdata.dir_alice(UserID_alice,"key.txt")
        read=open(path_alice, 'r')
        data=read.readlines()
        read.close()
        data2={}
        for i in range(len(data)):
            linelist=data[i].split(" ",2)
            data2[int(linelist[0])]=(linelist[1],eval(linelist[2]))
        #print(data2)
        return data2
        
##############################################################################
#                             GUI
##############################################################################

#------------------------------------------------------------------------------
#GUI Matrix convenience
#------------------------------------------------------------------------------

class GUImatrix:
    def grid_hor(frmlist,col):
        #give a list frm objects
        for i in range(len(frmlist)):
            frmlist[i].grid(row=i,column=col,sticky="nsew")
    
    def grid_vert(frmlist,row):
        #give a list frm objects
        for i in range(len(frmlist)):
            frmlist[i].grid(row=row,column=i,sticky="nsew")
    
    def grid_adjuste(x,rows,cols):
        #input a list of rows and cols
        #e.g. [[1,2],[1,10]], where 1 is the row 2 and 10 are the weights
        #adjust grid when resized
        #https://infohost.nmt.edu/tcc/help/pubs/tkinter/web/grid-config.html
        for i in range(len(rows)):
            x.grid_rowconfigure(rows[i][0], weight=rows[i][1])
        for i in range(len(cols)):
            x.grid_columnconfigure(cols[i][0], weight=cols[i][1])

#------------------------------------------------------------------------------
#GUI Main
#------------------------------------------------------------------------------

#keyflow chema
#            1: Asuuming there is no key created in the local file system
#                 X: occurs if 
#                    -keyfile was deleted (we may assume that the keyfile is
#                       not deleted during client application running
#                    -account is created
#              ,one must create this key and save it in the keyfile
#               so that this key can be sent to the server

#            2: The key must be created the following way:
#               In the server there must be keyID file, which stores the last 
#               keyID created                
#               This is necessary, as if client1 deletes his keys, client2 might
#               want to send a message with one of the deleted keys -he might not know
#               ,which client1 can't decrypt then- or will decrypt with a key woth wong 
#               assigned keyID
#               -client1 must therfore make a server request get the last keyID
#                and create an KeyID+1
#               -then he can create a key send the key and keyID+1 to the server
                 


class GUI:
    def __init__(self):
        
        #server ip adress and port
        self.j=ioserver(FileExtractIP(),"8000")
        
        #initial mehtod 
        self.crypto_method="rsa"
        
        #font for headings:
        self.bg="grey70"#"cadet blue"
        self.headFont=('times',14)
        
        #button Font
        self.buttonFont=('times',14, 'italic')
        self.buttonColor="white smoke" #"LightSteelBlue3" #
        self.buttonRelief="flat"
        #self.oldset=set()
        
        #some image 
        self.wrkdir = os.path.dirname(__file__)
        self.icon_path=os.path.join(self.wrkdir,"Icons","icon.gif" )
        
        #is a dictionary buffering all incomming messages
        self.chat_buffer={}
        
        #start Cryptograph: Login
        self.login_win()
        
    def pubkey_generate(self):
        # generates a new public key and prints it to the server
        
        #initialise new public keys
        
        #get last KeyID from server
        UserID_send=json.dumps({"UserID_alice": self.UserID_Alice})
        server_key=self.j.useroperation(UserID_send,"GETALICEKEYID")["keyID"]
        keyID_alice=server_key
        #create new KeyID
        keyID_alice=keyID_alice+1
        
        #----------------------------------------------------------------------
        #create a new public key for alice
        #----------------------------------------------------------------------
        method_alice=self.crypto_method
        key_alice=Crypto_method.Keys(method_alice) ##alice public key
        UserID_alice=self.UserID_Alice
        key_alice_private=key_alice[1]
        USRdata.store_keys(UserID_alice,str(keyID_alice),method_alice,str(key_alice_private))
        self.keys_buffer.update({keyID_alice: (method_alice,key_alice_private)})
        
        #----------------------------------------------------------------------
        #send data to server
        #----------------------------------------------------------------------
        data={'senderID': UserID_alice,'publickeys': key_alice[0], 'keyID_alice': keyID_alice, "method": method_alice}
        self.j.push(UserID_alice,data,"POSTKEY")
        
    def bob_initialice(self,UserID_alice,UserID_bob):
        USRdata.createFilestru(UserID_alice,UserID_bob)
        if not(UserID_bob in self.chat_buffer):
            self.chat_buffer[UserID_bob]=[]    
            
        
    def chat_update_init(self, UserID_alice,list_UserIDs_bob):
        
        for i in range(len(list_UserIDs_bob)):
            
            #initialise filesystem of bob (under alice)
            self.bob_initialice(UserID_alice,list_UserIDs_bob[i])
            
            #------------------------------------------------------------------
            #print chat history
            #------------------------------------------------------------------
            #1.st load chathistory, dated while client was offline from the server
            mess_list=USRdata.extract_allMessage(UserID_alice,list_UserIDs_bob[i])
            #2.nd load message_buffer
            self.chat_buffer[list_UserIDs_bob[i]].extend(mess_list)
            self.keys_buffer=USRdata.extract_keys(UserID_alice)
            #3.rd input_make_bob these messages
            if self.UserID_Bob==list_UserIDs_bob[i]:
                for ii in range(len(mess_list)):
                    self.iot.insert(tk.END,mess_list[ii][1])
                # scroll down to end of window
                self.iot.see(tk.END)
                
    def chat_update(self,UserID_alice, list_UserIDs_bob):
        #print(self.chat_buffer)
        #write a function creating a list contaning all messenge keys "
        # i.e "2019-05-29 18:30:59.099567" 
        #after every server_update compare those lists
        #and if the list is alterd, print the contents to the gui
        #of the matheamtical complement (set difference) of the old set to the new list
        
        #essential, as otherwise messanges no messages would income
        for i in range(len(list_UserIDs_bob)):
            #must be initialiced each loop as new bobs may have been created
            #also inside bob_initialise this Initialisation will only take place if it hasn't been before
            self.bob_initialice(UserID_alice,list_UserIDs_bob[i])
            
            
            try:
                #try is need, as if in json file on the server
                #under UserID_bob no UserID_alice exists
                #this will couse an error
                
                #------------------------------------------------------------------
                #get content bob since last localy saved message 
                #------------------------------------------------------------------
                lastTime=USRdata.extract_lastTime(UserID_alice,list_UserIDs_bob[i])
                #print(lastTime)
                content=self.j.useroperation(json.dumps({"UserID_bob":list_UserIDs_bob[i],"UserID_alice":UserID_alice, "timedate":lastTime}),"GETMESSAGES")["messages"]
                
                #------------------------------------------------------------------
                #handle content message by message 
                #------------------------------------------------------------------
                for ii in range(len(content)):
                    message_chiffre=content[ii][1]
                    message_time=content[ii][0]
                    
                    #1: Find Private key id in server-content 
                    message_privkey_id=int(content[ii][2])
                    #print(message_privkey_id)
                    
                    #2 Find message private Key inside key.txt file
                    #extract from file command here
                    keys=self.keys_buffer
                    #print(keys)
                    #exception here, if keyId does not exist
                    #print "Cryptograph>>  Decryption not possible- private key does not exist"
                    try:
                        crypto_method_bob=keys[message_privkey_id][0]
                        message_privkey=keys[message_privkey_id][1]
                        
                        print("method:",crypto_method_bob)
                        #print("key",message_privkey)
                        #decrypt at this configurations
                        message_decryp=Crypto_method.Decrypt(crypto_method_bob,message_chiffre,message_privkey)
                        
                        #buffer & insert  Message (and store last Message date)
                        self.input_make_bob(message_decryp,message_time,UserID_alice,list_UserIDs_bob[i])
                    except Exception: 
                        traceback.print_exc() #prints error message
                        #self.input_make_bob("Decryption not possible- private key may not exist",message_time,UserID_alice,list_UserIDs_bob[i])
            except:
                pass
                
        
        #change this (milliseconds) if update is to slow- however performance might increase
        chat_update_period=2000
        
        self.init.after(chat_update_period, lambda: self.chat_update(UserID_alice,list_UserIDs_bob))

    def input_make_alice(self,message,UserID_alice,UserID_bob):
        #prints the message "message" from User "namevar" to the gui
        #if send==True the message is printed to the server
        message_print=UserID_alice+">> "+message+'\n'
        
        nowtimedate=str(datetime.datetime.now())
        
        self.iot.insert(tk.END,message_print)
        self.iot.see(tk.END) # scroll down to end of window
        self.chat_buffer[UserID_bob].append([nowtimedate,message_print])
        self.input_send(message,UserID_alice,UserID_bob,nowtimedate)
        USRdata.store_Message(UserID_alice,UserID_bob,message_print,nowtimedate)
    
    def input_make_bob(self,message,message_time,UserID_alice,UserID_bob):
        #prints the message "message" from User "UserID_bob" to the gui
        message_print=UserID_bob +">> "+message+'\n'
        print("message", message)
        
        self.chat_buffer[UserID_bob].append([message_time,message_print])
        USRdata.store_Message(UserID_alice,UserID_bob,message_print,message_time)
        #it should just printout the message, if its one of the courrent chat partner 
        #(the current Listbox entry)
        if self.UserID_Bob==UserID_bob:
            self.iot.insert(tk.END,message_print)
            # scroll down to end of window
            self.iot.see(tk.END)
        #finally store the time of the last server extraction from bob
        USRdata.store_lastTime(UserID_alice,UserID_bob,message_time)
        
    def input_send(self,message,UserID_alice,UserID_bob,nowtimedate):
        
        #get last KeyID from server
        UserID_send=json.dumps({"UserID_alice": self.UserID_Alice})
        server_key=self.j.useroperation(UserID_send,"GETALICEKEYID")["keyID"]
        keyID_alice=server_key
        #create new KeyID
        keyID_alice=keyID_alice+1
        
        #----------------------------------------------------------------------
        #Encrypt message for bob
        #----------------------------------------------------------------------
        #get key from bob
        server_content=self.j.pull(UserID_bob)
        #print(server_content)
        #maybe write a request-method in the MyHTTPRequestHandler in the server.py file, so in order to make this more efficient
        key_bob=server_content["mykey"]["publickey"]
        method_bob=server_content["mykey"]["method"]
        keyID_bob=server_content["mykey"]["keyID"]
        message_chiffre=Crypto_method.Encrypt(method_bob,message,key_bob)
        
        #----------------------------------------------------------------------
        #create a new public key for alice
        #----------------------------------------------------------------------
        method_alice=self.crypto_method
        key_alice=Crypto_method.Keys(method_alice) ##alice public key
        key_alice_private=key_alice[1]
        #store public key of alice locally
        keyID_alice_str=str(keyID_alice)
        USRdata.store_keys(UserID_alice,keyID_alice_str,method_alice,str(key_alice_private))
        self.keys_buffer.update({keyID_alice: (method_alice,key_alice_private)})
        #print(self.keys_buffer)
        
        #----------------------------------------------------------------------
        #send data to server
        #----------------------------------------------------------------------
        data={'senderID': UserID_alice, 'receiverID': UserID_bob ,'publickeys': key_alice[0], 'keyID_alice': keyID_alice, 'keyID_bob': keyID_bob , "method": method_alice, 'message': message_chiffre, "nowtimedate":nowtimedate}
        self.j.push(UserID_alice,data,"POST")
        
    def input_get(self):
        #get input inserted in the editor at command "Enter Key" or Button
        message=self.message.get(1.0, tk.END)
        self.message.delete(1.0,tk.END)
        return message

    
    def login_win(self):
        
        self.login_win=tk.Tk()
        self.login_win.title("Cryptograph-Login")
        self.login_win.resizable(width=False, height=False)
        
        #----------------------------------------------------------------------
        #Frame Head
        #----------------------------------------------------------------------
        
        self.login_frame_head=tk.Frame(self.login_win,bd=10)
        frm_h=self.login_frame_head
        self.icon_img = tk.PhotoImage(file=self.icon_path)
        photo=tk.Label(frm_h, image = self.icon_img)
        l1txt1 ='Login to Cryptograph'
        l1 = tk.Message(self.login_frame_head, width=1000, text=l1txt1)
        hline=tk.Canvas(self.login_frame_head, height=20)
        hline.create_line(5, 5, 500, 5)
        l1.config(font=self.headFont)
        
        GUImatrix.grid_hor([l1,hline,photo],1)
        
        #----------------------------------------------------------------------
        #Frame Options
        #----------------------------------------------------------------------
        
        frm_o=self.login_frame_opt=tk.Frame(self.login_win,bd=10)
        l2txt1='Username:'
        l3txt1='Password:'
        l2 = tk.Message(self.login_frame_opt, width=1000, text=l2txt1)
        l3 = tk.Message(self.login_frame_opt, width=1000, text=l3txt1)
        
        GUImatrix.grid_hor([l2,l3],1)
        
        log=self.login_usrname=tk.Entry(self.login_frame_opt)
        pswd=self.login_password=tk.Entry(self.login_frame_opt,show='*')
        
        GUImatrix.grid_hor([log,pswd],2)
        
        #----------------------------------------------------------------------
        #Frame Foot
        #----------------------------------------------------------------------
        
        frm_f=self.login_frame_foot=tk.Frame(self.login_win,bd=10)
        
        #initialise check variable for login
        self.login_check_bool=False
        
        button=tk.Button(self.login_frame_foot,text='Make Login',command=lambda: self.login_make(),relief=self.buttonRelief,bg=self.buttonColor, font=self.buttonFont)
        button2=tk.Button(self.login_frame_foot,text='Create Account',command=lambda: self.login_win_upd(),relief=self.buttonRelief,bg=self.buttonColor, font=self.buttonFont)
        
        GUImatrix.grid_vert([button,button2],1)
        
        hline2=tk.Canvas(self.login_win, height=10)
        hline2.create_line(20, 5, 500, 5)
           
        #----------------------------------------------------------------------
        #Put it together
        #----------------------------------------------------------------------
        
        self.login_str1 = tk.StringVar()
        self.l4 = tk.Label(self.login_win, textvariable=self.login_str1)
        
        GUImatrix.grid_hor([frm_h,frm_o,self.l4,hline2,frm_f],1)
        
        self.login_win.mainloop()
    
    def login_win_upd(self):
        l4txt1="Reenter Password"
        l4 = tk.Message(self.login_frame_opt, width=1000, text=l4txt1)
        l4.grid(row=3,column=1,sticky="nsew")
        pswd2=tk.Entry(self.login_frame_opt,show='*')
        pswd2.grid(row=3,column=2,sticky="nsew")
        button3=tk.Button(self.login_frame_foot,text='Confirm Account',command=lambda: self.make_account_server() ,relief=self.buttonRelief,bg=self.buttonColor, font=self.buttonFont)
        button3.grid(row=1,column=1,sticky="nsew")
        
    def login_make(self):
        usrname=self.login_usrname.get()
        password=self.login_password.get()
        self.login_check(usrname,password)
        if self.login_check_bool==True:
            
            self.login_win.destroy()
            #the following are IMPORTANT initalisations
            self.UserID_Alice=usrname
            #self.pubkey_generate()
            self.home()
            #Note:
            #you are allowed to (create instance of class tk.Tk())
            #create instance, mainloop instance, create another instance, mainloop other instance
            #for some reason however
            #Create instance, Create another instance, create mainloop of instance, create mainloop of other instance
            #gives an exception error

    def make_account_server(self):
        #input is string
        UserID_bob=self.login_usrname.get()
        dict_py={"UserID_bob": UserID_bob}
        dict_js=json.dumps(dict_py)
        exists=self.j.useroperation(json.dumps({"UserID":UserID_bob}), "FINDUSER")
        exists=exists["exists"]
        #print(exists)
        if exists==False:
            #create an "account" - so a .json file on the server side
            self.j.useroperation(dict_js,"CREATEACCOUNT")
            self.login_make()
        else:
            self.login_str1.set("This account already exists")

    def login_check(self,username, passphrase):
        #checks if the login makes sence /is correct
        #check if username exists:
        adress=self.j.ip_adress_format()+username +".json"
        #this status_code trick is snippled from
        #https://stackoverflow.com/questions/16778435/python-check-if-website-exists
        direxists = requests.get(adress)
        if direxists.status_code == 200:
            self.login_check_bool=True
        else:
            self.login_check_bool=False
            self.login_str1.set("This account does NOT exist")
        #print(self.login_check_bool)
        #if 
        #check if passphrase is correct:
        #for the beginning the passphrase will just be the username
        #if 
    
    def input_userSwitch(self):
        #A function which switches the text window output by
        
        #current UserID of communication partner
        listbox_row=self.lst.curselection()[0]
        #print("listbox ", listbox_row)
        UserID_bob_curr=self.contacts[listbox_row]
        
        #delete contents of Textbox
        self.iot.delete('1.0', tk.END)
        
        #print buffered messages of user: User_ID_bob_curr
        try:
            buffer=self.chat_buffer[UserID_bob_curr]
            if buffer !=[]:
                for i in range(len(buffer)):
                    self.iot.insert(tk.END,buffer[i][1])
                # scroll down to end of window
                self.iot.see(tk.END)
        except:
            ...
        
        #Set self.UserID_Bob
        self.UserID_Bob=UserID_bob_curr

    def home(self):
        
        #list of contacts of user
        UserID_send=json.dumps({"UserID_alice": self.UserID_Alice})
        contacts_list=self.j.useroperation(UserID_send,"GETCONTACTLIST")["contacts"]
        self.contacts=contacts_list
        
        #initialise self.UserID_Bob - the current communication partner
        self.UserID_Bob=self.contacts[0]
        #so there must be at least one existing partner
        
        
        #----------------------------------------------------------------------
        #GUI
        #----------------------------------------------------------------------
        home_root = tk.Tk()
        self.init=home_root
        #create platform independant path
        #https://stackoverflow.com/questions/6036129/platform-independent-file-paths
        try:
            self.init.tk.call('wm', 'iconphoto', self.init._w, self.icon_img)
        except:
            ...
        
        
        #i found the above here:
        #https://stackoverflow.com/questions/11176638/tkinter-tclerror-error-reading-bitmap-file
        self.init.title("Cryptograph")
        GUImen.menubar(self.init,self, self.headFont)
        
        
        #----------------------------------------------------------------------
        #main rank
        #----------------------------------------------------------------------        
        self.home_frame_top=tk.Frame(self.init)
        self.home_paned=tk.PanedWindow(self.init,bd=10)
        self.home_paned.configure(bg=self.bg)

        #----------------------------------------------------------------------
        #paned 1'st order
        #----------------------------------------------------------------------        
        self.home_frame1=tk.Frame()
        self.home_frame2=tk.Frame()
        
        #----------------------------------------------------------------------
        #paned 2'nd order
        #----------------------------------------------------------------------        
        self.home_subpaned=tk.PanedWindow(self.home_frame2,orient="vertical")
        self.home_subpaned.configure(bg=self.bg)
        self.home_subpaned.pack(fill="both", expand=True)
        self.home_subframe2_1=tk.Frame(self.home_frame2)
        self.home_subframe2_2=tk.Frame(self.home_frame2)
                
        #----------------------------------------------------------------------
        #chat list
        #----------------------------------------------------------------------        
        self.lst = tk.Listbox(self.home_frame1)
        self.lst.bind('<<ListboxSelect>>',lambda x: self.input_userSwitch())
        #don't ask me why but here you will need an "x" after lambda and
        #before ":"
        #https://stackoverflow.com/questions/16215045/typeerror-lambda-takes-no-arguments-1-given
        
        self.lst.grid(row=1,column=1,sticky="nsew")
        
        self.contact_show_update()
        
        #----------------------------------------------------------------------
        #button
        #----------------------------------------------------------------------        
        button=tk.Button(self.home_frame1,text='Encrypt/send Message ✍', command= lambda: self.input_make_alice(self.input_get(),self.UserID_Alice,self.UserID_Bob),bg=self.buttonColor ,relief=self.buttonRelief, font=self.buttonFont) # insert command=Encryptionfunction
        #used a unicode character for this:
        #https://unicode-table.com/en/270D/
        #the remainder code line works with "lamda" without it dosen't however I don't know why
        button.grid(row=2,column=1,sticky="nsew")
        
        #----------------------------------------------------------------------
        #output window
        #----------------------------------------------------------------------        
        self.iot=tk.Text(self.home_subframe2_1,wrap=tk.WORD)
        self.iot.grid(row=1,column=1,sticky="nsew")
        
        #----------------------------------------------------------------------
        #input window
        #----------------------------------------------------------------------        
        self.message=tk.Text(self.home_subframe2_2, height=4)
        self.message.grid(row=1,column=1,sticky="nsew")
        
        #----------------------------------------------------------------------
        #scrollbar
        #----------------------------------------------------------------------
        self.home_scrollbar=tk.Scrollbar(self.home_subframe2_1, orient=tk.VERTICAL, command=self.iot.yview, width=15)
        self.home_scrollbar.grid(row=1,column=2,sticky="nsew")
        self.iot['yscrollcommand']=self.home_scrollbar.set
        
        self.home_scrollbar_mes=tk.Scrollbar(self.home_subframe2_2, orient=tk.VERTICAL, command=self.message.yview, width=15)
        self.home_scrollbar_mes.grid(row=1,column=2,sticky="nsew")
        self.message['yscrollcommand']=self.home_scrollbar_mes.set
        
        self.home_scrollbar_bobs=tk.Scrollbar(self.home_frame1, orient=tk.VERTICAL, command=self.lst.yview, width=15)
        self.home_scrollbar_bobs.grid(row=1,column=2,sticky="nsew")
        self.lst['yscrollcommand']=self.home_scrollbar_bobs.set
        
        #----------------------------------------------------------------------
        #status widget
        #----------------------------------------------------------------------
        hf_txt1="Loged in as: "+self.UserID_Alice
        hf_txt2="date: "+str(datetime.datetime.now())
        self.hf_txt3= tk.StringVar()
        status1=tk.Label(self.home_frame_top,text=hf_txt1)
        status2=tk.Label(self.home_frame_top,text=hf_txt2)
        status3=tk.Label(self.home_frame_top,textvariable=self.hf_txt3)
        self.hf_txt3.set("method: "+self.crypto_method)
        GUImatrix.grid_hor([status1,status2,status3],0)
        
        #----------------------------------------------------------------------
        #adjust the grid
        #----------------------------------------------------------------------
        #self.grid_adjuste(self.init,[[1,1]],[[1,1],[2,10]])
        GUImatrix.grid_adjuste(self.init,[[0,0],[1,1]],[[0,1]])
        GUImatrix.grid_adjuste(self.home_frame1,[[1,1],[2,0]],[[1,1]])
        GUImatrix.grid_adjuste(self.home_subframe2_1,[[1,1]],[[1,1],[2,0]])
        GUImatrix.grid_adjuste(self.home_subframe2_2,[[1,1]],[[1,1],[2,0]])
        
        #----------------------------------------------------------------------
        #Put it together
        #----------------------------------------------------------------------        
        self.home_frame_top.grid(row=0,column=0,sticky="nsew")
        self.home_paned.grid(row=1,column=0,sticky="nsew")
        
        self.home_paned.add(self.home_frame1,sticky="nsew",stretch="always")
        self.home_paned.add(self.home_frame2,sticky="nsew")
        
        self.home_subpaned.add(self.home_subframe2_1,sticky="nsew",stretch="always")
        self.home_subpaned.add(self.home_subframe2_2,sticky="nsew")
        
        #----------------------------------------------------------------------
        #Chat Update
        #----------------------------------------------------------------------        
        #initialise chat - get from server
        
        self.chat_update_init(self.UserID_Alice,self.contacts)
        
        self.pubkey_generate()
        
        self.chat_update(self.UserID_Alice,self.contacts)
                
        self.end()
      

    def men_addcontact_server(self,UserID_bob):
        #write serverrequest to add user to account (.json file)
        
        data1=json.dumps({"UserID":UserID_bob})
        exists=self.j.useroperation(data1,"FINDUSER")["exists"]
        
        if exists==True:
            data2=json.dumps({"UserID_bob":UserID_bob,"UserID_alice": self.UserID_Alice})
            self.j.useroperation(data2,"ADDCONTACT")
            
            #update chatlist
            if UserID_bob not in self.contacts:
                self.contacts.append(UserID_bob)
            self.contact_show_update()
            #update contacts -array        
    
    def contact_show_update(self):
        #get json file contacts and insert contents here:
        
        #clear list
        self.lst.delete(0,tk.END)
        
        #input changed contacts in listbox
        for x in range(len(self.contacts)):
            self.lst.insert(tk.END,self.contacts[x])
        
    
    def config_encrypt(self,encryptcode):
        self.crypto_method=encryptcode.get()
        self.hf_txt3.set("method: "+self.crypto_method)
    
    def end(self):
        self.init.mainloop()

#------------------------------------------------------------------------------
#GUI Menue
#------------------------------------------------------------------------------

class GUImen:

    def menubar(motherObj,selfobj,font):
        menubar=tk.Menu(motherObj)
        filemenu=tk.Menu(menubar,tearoff=0)
        menubar.add_cascade(label='File',menu=filemenu)
        filemenu.add_command(label='Quit',command=motherObj.quit())
        helpmenu=tk.Menu(menubar,tearoff=0)
        menubar.add_cascade(label='Help',menu=helpmenu)
        helpmenu.add_command(label='About',command=lambda: GUImen.men_about(motherObj,font))
        helpmenu.add_command(label='Help',command= lambda: GUImen.men_help(font))
        configure=tk.Menu(menubar,tearoff=0)
        menubar.add_cascade(label='Config',menu=configure)
        configure.add_command(label='Add contact',command=lambda: GUImen.men_addcontact(selfobj,font))
        #configure.add_command(label='change default server',command=lambda: GUImen.men_serverconf(selfobj))
        configure.add_command(label='Encryption Algorithm',command= lambda: GUImen.men_encryptconf(selfobj,font))
        motherObj.config(menu=menubar)

    def men_help(headFont):
        men=tk.Tk()
        men.title("Cryptograph-Help")
        men.resizable(width=False, height=False)
        text1='Cryptograph-Helppage:'
        text2='The help documentation can be found at:'
        text3='https://github.com/stephanb15/Cryptograph/wiki'
        msg1 = tk.Message(men,width=1000, text=text1)
        msg2 = tk.Message(men,width=1000, text=text2)
        msg3 = tk.Message(men,width=1000, text=text3)
        msg1.config(font=headFont)
        
        GUImatrix.grid_hor([msg1,msg2,msg3],1)
        
        men.mainloop()
        
    def men_about(motherObj,headFont):
        men=tk.Tk()
        #men.geometry("500x500")
        men.title("Cryptograph-About")
        men.resizable(width=False, height=False)
        GUImatrix.grid_adjuste(motherObj,[[1,1]],[[1,1]])
        l1txt1='This is a communication software with built in cryptographic algorithms.'
        l1txt2='It was created in 2019 by a team of students at the university of Vienna'
        l1txt3='(faculty of matheamtics) as part of a programming practical.'
        l2txt1='Jakob Lanser   a11806538@unet.univie.ac.at'
        l2txt2='Saifullah Totakhel a11713253@unet.univie.ac.at'
        l2txt3='Stephan Bornberg   a01506156@unet.univie.ac.at'
        l1 = tk.Message(men ,width=1000, text='''Cryptograph 1.0:''')
        l2 = tk.Message(men, width=1000, text=l1txt1+'\n'+l1txt2+'\n'+l1txt3)
        l3 = tk.Message(men, width=1000, text='Authors names:')
        l4 = tk.Message(men, width=1000, text=l2txt1+'\n'+l2txt2+'\n'+l2txt3)
        l1.config(font=headFont)
        l3.config(font=('times',12, 'bold'))
        
        GUImatrix.grid_hor([l1,l2,l3,l4],1)
        
        men.mainloop()
        
    def men_addcontact(selfobj,headFont):
        men=tk.Tk()
        men.title("Cryptograph-Add contact")
        men.resizable(width=False, height=False)
        l1txt1 ='Add Contacts'
        l2txt1='Input an exististing username.'
        l2txt2='(If the username does not exists de Feedback dialog will print an error)'
        l3txt1='Feedback:'
        l1 = tk.Message(men, width=1000, text=l1txt1)
        l2 = tk.Message(men, width=1000, text=l2txt1+'\n'+l2txt2)
        l3 = tk.Message(men, width=1000, text=l3txt1)
        
        hline=tk.Canvas(men, height=20)
        hline.create_line(5, 5, 500, 5)
        hline2=tk.Canvas(men, height=20)
        hline2.create_line(5, 5, 500, 5)
        
        usrname=tk.Entry(men)
        button=tk.Button(men,text='Find user', command= lambda: selfobj.men_addcontact_server(usrname.get()))
        l1.config(font=headFont)
        
        GUImatrix.grid_hor([l1,hline,l2,hline2,usrname,button,l3],1)
        
        #Write some input box add contact and a button 
        #if contact exists add the contact- else print: contact doesn't exists
        #if wrinting it advanced use some search function
        men.mainloop()
    
    def men_serverconf(selfobj):
        men=tk.Tk()
        men.title("Cryptograph-Change Default server")
        men.resizable(width=False, height=False)
        l1txt1 ='Insert http address here'
        l1 = tk.Message(men, width=1000, text=l1txt1)
        address=tk.Entry(men)
        button=tk.Button(men,text='Configure server')#, command= lambda: self.input_get())
        l1.config(font=selfobj.headFont)
        
        GUImatrix.grid_hor([l1,address,button],1)
        
        men.mainloop()
        
    def men_encryptconf(selfobj,font):
        #In order to choose from different encryption algorithm, a input format will
        #be given. And one can create his one algorithm by composition of
        #predefined Encryption algoritms
        ## Syntax:
        # ":" is a seperator which stands for the "little o symbol"
        # which is commonly used in mathematics to notate compostions of functions
        # f and g, thus
        # f:g is the composition of f taking g as argument
        # one can create compositions of infinite length by reusing this notation
        # and by the knowledge, that ":" is associativ
        # Thus for example f:g:e:g:f:g:h
        # is a "more conplex" algorithm
        #or more genreally
        # Let (f_{i}) be a finite sequence where each part of the sequence is an
        # element of a Set of Cryptographic Functions (which I will defined later accuratly)
        # I state that this Programm can Encrypt by computing Compositions of the form
        # f_{1}:f_{2}:f_{3}:...:f_{n} 
        # now the Set of Encryption Functions (for this programm)
        # can be found below (Where each function of the Set is a Function of the python class defined below)
        
        #Here I will assign names for these functions
        # RSA:="in class Encrypt function RSA(prime1, prime2)"
        # where for the beginning prime1, prime2, are to be fixed primes
        # Later I will create more sophisticated algorithms
    

        #The last paragraph is not exact i will change it later

        men=tk.Tk()
        men.title("Cryptograph-Change Encryption Algorithm")
        men.resizable(width=False, height=False)
        l1txt1 ='Cryptographic Configurations'
        l2txt1 ='Insert Algorithm explenation here'
        l3txt1 ='(See the help menue)'
        l1 = tk.Message(men, width=1000, text=l1txt1)
        l2 = tk.Message(men, width=1000, text=l2txt1)
        l3 = tk.Message(men, width=1000, text=l3txt1)
        encryptcode=tk.Entry(men)
        button=tk.Button(men,text='Configure Encryption', command= lambda: selfobj.config_encrypt(encryptcode))
        l1.config(font=font)
        l1.grid(row=1,column=1,sticky="nsew")
        l2.grid(row=2,column=1,sticky="nsew")
        l3.grid(row=3,column=1,sticky="nsew")
        encryptcode.grid(row=4,column=1,sticky="nsew")
        button.grid(row=5,column=1,sticky="nsew")
        men.mainloop()

##############################################################################
#                             Client-Server
##############################################################################
       
class ioserver:
    def __init__(self,serveradressHome,PortHome):
        self.serveradressHome=serveradressHome
        self.PortHome=PortHome
        #for testing- use the localhost
        #self.serveradressHome="http://localhost:8000/"
    
    def ip_adress_format(self):
        path="http://"+self.serveradressHome+":"+self.PortHome+"/"
        return path
    
    def pull(self,UserID_sender):
        #get the pulblic Key, messages from user :UserID
        #https://docs.python.org/3/howto/urllib2.html
        #https://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script
        pathHome=self.ip_adress_format()+UserID_sender +".json"
        with urllib.request.urlopen(pathHome) as response:
            data=response.read().decode()
            outptdict=json.loads(data)
        return outptdict
    
    def push(self,UserID_sender,data, method):
        #data must be an dictionary of 
        #the userID dedicated to you
        #create a json string from python dictionary
        data=json.dumps(data)
        #create byte data
        data=bytes(data,encoding='utf8')
        #print(data)
        pathHome=self.ip_adress_format()+UserID_sender +".json"
        pushed = urllib.request.Request(url=pathHome, data=data,method=method)
        try:
            urllib.request.urlopen(pushed)
        except:
            #by that I prevent the error message
            #"raise RemoteDisconnected("Remote end closed connection withou"
            #aldough writing to the server now works without a client error 
            #this is a dirty solution
            #print("Server Communication Error")
            ...
        
    def useroperation(self,data,method):
        #pushed = urllib.request.Request(url=pathHome, data=data,method="FINDUSER")
        client2=http.client.HTTPConnection(self.serveradressHome,port=self.PortHome)
        client2.request(method=method,body=data,url="")
        exists2={"1":"1"} #initialice
        try:
            #this is a foolish work around but ive got no idea how to solve this else
            #https://stackoverflow.com/questions/4308182/getting-the-exception-value-in-python
            #https://stackoverflow.com/questions/27619258/httplib-badstatusline
            #the reason for this error arriving is that i might not adapt to http standard accordnig to forums, source
            instance=client2.getresponse()
            instance.read()
        except http.client.BadStatusLine as exists:
            exists2=json.loads(str(exists))
            #print("exists2: ",exists2)
        return exists2
    
class virtstaticip:
    #this class handles pull task(s) for maintaining a virtual static ip
    #the ip of my home server is not static,
    #by the application sendip.py the ip adress is send to the uni-server 
    def __init__(self):
        self.serveradressUni="https://www.unet.univie.ac.at/~stephanb15/Applications/Cryptograph/"
    def pull(self):
        pathHome=self.serveradressUni+".json"
        with urllib.request.urlopen(pathHome) as response:
            data=response.read().decode()
            outptdict=json.loads(data)
        return outptdict

##############################################################################
#                             Cryptography
##############################################################################

class Crypto_method:
    #This class switches the cryptographic algorithmus.
    #assigned by the method_str string,
    #The messaeg_str is assumed to be of countable length
    #(Methodes Encrypt_large, Decrypt_Large in class RSA where created for that reason)
    
    def Assign_number(message_str):
        #Maybe i should make this function more general in the future
        # For now the first 99999 Unicode characters can be encrypted
        #for the reason, that its very unlikely, that the first 100 characters will be 
        # used very much more likely than the following (assuming english conversation,
        #this doesn't hold for asian communication), this function might be inefficient
        #furthermore it shouldn't be used with RSA but only in combination with OEAP --security risk
        
        message_numb=""
        
        for i in range(len(message_str)):
            
            numb_unform=ord(message_str[i])
            str_unform=str(numb_unform)
            len_numb=len(str_unform)
            
            #create a formated string
            if len_numb > 99999:
                str_form="65533" #this is the unicode for replacment character, 65533==ord("�")
                # https://en.wikipedia.org/wiki/Specials_(Unicode_block)
            else:
                #create a block "0...ord(char)"
                len_zero_block=5-len_numb
                zero_block="0"*len_zero_block
                str_form=zero_block+str_unform ## create the formated string
                #one can proof easily, that str_form has length 5 (which is what I wanted)
                # PROOF: the addition theorem for length of cantenation is len(a||b)=len(a)+len(b)
                # so it follows, that len(str_form)=len(zero_block)+len(str_unform)=5-len_numb+len(str_unform)=5
                # which makes sence (to use length 5)  as its compact in the sence of, that len("99999")=5
            message_numb+=str_form
        
        return message_numb
        
    def Assign_charlst(message_numb):
        #This is the inverse function of methode Assign_number
        message_str=""
        for i in range(int(len(message_numb)/5)): ## the same block length is used here: 5
            char_numb=message_numb[5*i:5*i+5]
            char_int=int(char_numb)
            char_chr=chr(char_int)
            message_str+=char_chr
        #remove "\00" in message_str (but find out why they create)
        message_str=message_str.replace("\00","")
        return message_str
    
    def Keys(method_str):
        if method_str== "rsa":
            keys1=RSA.Keys_auto()
            keys=keys1
        elif method_str== "trans":
            trans=Transposition()
            key=trans.key
            keys=[key, key] #just random values since there are no keys fore these functions
        elif method_str== "sub":
            selfsub=Substitution()
            keys=[selfsub.subAlphabet,selfsub.subAlphabet]
        else:
            keys=[1,1]
        return keys
            
    def Encrypt(method_str, message_str, pubkey):
        # I don't use self here, becouse i don't like to restrict the application of this class function 
        # I use strings as input output bexouse some cry ptographic methodes other than rsa
        # don't have numeric chiffre (i.e Substitution, Transopostion)
        
        if method_str== "rsa":
            message_numb=Crypto_method.Assign_number(message_str)
            #print("mes", message_numb)
            chiffre=RSA.Encrypt_large(message_numb, pubkey, 24) #the length 19 should be made variable in the future
        elif method_str== "trans":
            trans=Transposition()
            trans.key=pubkey
            chiffre=trans.encrypt_Message(message_str)
        elif method_str== "sub":
            message_str=message_str.rstrip()
            selfsub=Substitution()
            selfsub.subAlphabet=pubkey
            chiffre=selfsub.encrypt_Message(message_str)
            #print("chiffre",chiffre)
        else:
            #if the method is incorrect/ not given, there will be an identity en/decryption-
            chiffre=message_str
        return chiffre
        
    def Decrypt(method_str,chiffre,privkey):
        # I don't use self here, becouse i don't like to restrict the application of this class function
        if method_str== "rsa":
            message_str=RSA.Decrypt_large(chiffre, privkey,24)
            message_str=Crypto_method.Assign_charlst(message_str)
        elif method_str=="trans":
            trans=Transposition()
            trans.key=privkey
            message_str=trans.decrypt_Message(chiffre)
        elif method_str=="sub":
            selfsub=Substitution()
            selfsub.subAlphabet=privkey
            message_str=selfsub.decrypt_Message(chiffre)
            #print("decrypted",message_str)
            message_str=message_str+"\n"
        else:
            #if the method is incorrect/ not given, there will be an identity en/decryption-
            message_str=chiffre
        return message_str



class OAEP:
    #Optimal Asymmetric Encryption Padding
    #https://de.wikipedia.org/wiki/Optimal_Asymmetric_Encryption_Padding
    def Keys():
        #there is only one private key
        k0=20
        #print(os.urandom(k0))

##############################################################################
#                             Main
##############################################################################

gui=GUI()


##############################################################################
#                             Testing
##############################################################################

###Testing Encryption

#mykeys=RSA.Keys_auto()#823,827)
#print(mykeys)
#testvalues=[1000000100000010000001000000]*10
#print([1000000]*1000)
#testvalues=[100000**10]*10

#I like to allow the first 1000000 unicode characters to be used for sending messages
# I'm afraid using large unicode unicode sets where most of these unicodes will unlikely be used for text messaging, might couse securitx risc
#without combination with some algorithm like OAEP

#I will block theses unicodes (mathematically speaking I will concatenate theses unicodes so that the resulting string is smaller than prime1*prime2)
# then I will apply OAEP-RSA

#I think its reasonable to create a characterset- map for each encryption technic, so as a general approach might be a security issue for a non- OAEP-RSA 
#encryption technique


#testvalues=[78544333333333333333986593733333333323412451245333333333333333333333326]
#for i in range(len(testvalues)):
#    mysterytext=RSA.Encrypt_large(testvalues[i],mykeys[0],25)
#    #mysterytext=g.Encrypt(testvalues[i],mykeys[0])
#    print(mysterytext)
#    plaintext=RSA.Decrypt_large(mysterytext, mykeys[1])
#    #text=g.Decrypt(mysterytext, mykeys[1])
#    print(plaintext)

    
#numb=Crypto_method.Assign_number("12str_%&/§f 劒 ▦ ꉨ Ꞥ ꡁ ∉") ##testing some "random" unicode characters
#print(numb)
#print(Crypto_method.Assign_charlst(numb))
#message="12str_%&/§f 劒 ▦ ꉨ Ꞥ ꡁ ∉3"
#keys=Crypto_method.Keys("rsa")
#chiffre=Crypto_method.Encrypt("rsa",message,keys[0])
#decryp=Crypto_method.Decrypt("rsa",chiffre,keys[1])
#print(decryp)


#j=ioserver("178.191.88.79","8000")
#print(j.useroperation(json.dumps({"UserID":"Mustermann"}),"FINDUSER"))
#print(j.useroperation(json.dumps({"UserID_bob":"mustermann","UserID_alice":"stephanb15", "timedate":'2019-07-03 17:19:23.164112'}),"GETMESSAGES"))


#print(hex(int(Crypto_method.Assign_number("Some normal length of a message- i might must compress this fomat somehow"))))
#d=Decrypt(mysterytext)
#readblmess=d.RSA(mykeys[1])
#print(readblmess)

#Testing Json


#output=j.pull("plain")
#print(output)

#output["message"]["Bob1"]="hAllO wORld"

