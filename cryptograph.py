import tkinter as tk
import json
import urllib.request
import requests
import os
import math
import datetime
import http.client

from lib.RSA import RSA
from lib.transposition import Transposition

##############################################################################
#                             Local FIles
##############################################################################

class USRdata():
    #This is a class handling user Data
    #like decrypted Messages etc
    wrkdir = os.path.dirname(__file__)
    
    def mkdir(path):
        #https://thispointer.com/how-to-create-a-directory-in-python/
        if not os.path.exists(path):
            os.mkdir(path)
    
    def mfile(path):
        if not os.path.isfile(path):
            open(path, 'w').close()
    
    def createFilestru(UserID_alice, UserID_bob):
        path_alice=os.path.join(USRdata.wrkdir,"usr",UserID_alice)
        USRdata.mkdir(path_alice)
        path_bob=os.path.join(USRdata.wrkdir,"usr",UserID_alice, UserID_bob)
        USRdata.mkdir(path_bob)
    
    
    def storeMessage(UserID_alice,UserID_bob,message,datetime):
        #messages must be an array of strings of format:
        #str(datetime.datetime.now())+" "+message
        USRdata.createFilestru(UserID_alice,UserID_bob)
        
        path_bob=os.path.join(USRdata.wrkdir,"usr",UserID_alice, UserID_bob,"messages.txt")
        write=open(path_bob, 'a')
        write.write(datetime+" "+message)
        write.close()
    
    def store_lastTime(UserID_alice,UserID_bob,datetime):
        #so in order to now the last recwived Message-Time of Bob
        path_bob=os.path.join(USRdata.wrkdir,"usr",UserID_alice, UserID_bob,"lastTime.txt")
        write=open(path_bob, 'w')
        write.write(datetime)
        write.close()
        
    def extract_lastTime(UserID_alice,UserID_bob):
        path_bob=os.path.join(USRdata.wrkdir,"usr",UserID_alice, UserID_bob,"lastTime.txt")
        read=open(path_bob, 'r')
        lastTime=read.readlines()
        read.close()
        return lastTime
        
    def extract_allMessage(UserID_alice,UserID_bob):
        path_bob=os.path.join(USRdata.wrkdir,"usr",UserID_alice, UserID_bob,"messages.txt")
        read=open(path_bob, 'r')
        buffer=read.readlines()
        buffer2=[]
        for i in range(len(buffer)):
            buffer2.append(buffer.split(" ",2))
            
        read.close()
        
        return buffer2
    

##############################################################################
#                             GUI
##############################################################################

class GUImatrix:
    def grid_hor(frmlist,col):
        #give a list frm objects
        for i in range(len(frmlist)):
            frmlist[i].grid(row=i,column=col,sticky="nsew")
    
    def grid_vert(frmlist,row):
        #give a list frm objects
        for i in range(len(frmlist)):
            frmlist[i].grid(row=row,column=i,sticky="nsew")

class GUI:
    def __init__(self):
        
        self.j=ioserver("178.191.88.79","8000")
        
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
        
        self.newset={}
        self.oldset={}
        
        self.login()
        
    def pubkey_generate(self):
        # generates a new public key and prints it to the server
        
        #initialise new public keys
        
        #create a new public key for alice
        keyID_alice=1
        method_alice="rsa"
        self.key_alice=Crypto_method.Keys(method_alice) ##alice public key
        UserID_alice=self.UserID_Alice
        data={'senderID': UserID_alice,'publickeys': self.key_alice[0], 'keyID_alice': keyID_alice, "method": method_alice}
        print(data)
        self.j.push(UserID_alice,data,"POSTKEY")
        
        
        
    def chat_update_init(self, UserID_alice,list_UserIDs_bob):
        
        #get all server contents from Bob
        for i in range(len(list_UserIDs_bob)):
            self.server_content=self.j.pull(list_UserIDs_bob[i])
            #sieve messages dedicated to Alice 
            self.oldset[list_UserIDs_bob[i]]=set(self.server_content["message"][UserID_alice].keys())
            
            #initialise buffer by creating lists dedicated to UserID-keys
            self.chat_buffer[list_UserIDs_bob[i]]=[]
            
            
            #print chat history
            
            #1.st load chathistory, dated while client was offline from the server
            
            #2.nd load message_buffer
            #3.rd input_make_bob these messages
            
            #get all contents (messages, contacts from server as initialised)
            #maybe for performance create a synchronisation algorithms to
            #save from big downloads, later
        
        
    def chat_update(self,UserID_alice, list_UserIDs_bob):
        print(self.chat_buffer)
        #write a function creating a list contaning all messenge keys "
        # i.e "2019-05-29 18:30:59.099567" 
        #after every server_update compare those lists
        #and if the list is alterd, print the contents to the gui
        #of the matheamtical complement (set difference) of the old set to the new list
        
        #essential, as otherwise messanges no messages would income
        for i in range(len(list_UserIDs_bob)):
            self.server_content=self.j.pull(list_UserIDs_bob[i]) ######## CHANGE PLAIN TO GENERAL USERID
            
            self.newset[list_UserIDs_bob[i]]=set(self.server_content["message"][UserID_alice].keys())
            #print(self.newset)
            difference=self.newset[list_UserIDs_bob[i]]-self.oldset[list_UserIDs_bob[i]]
            self.oldset[list_UserIDs_bob[i]]=self.newset[list_UserIDs_bob[i]]
            
            #order the differnce-set by date and print out the dedicated messages
            #, so the dictionary[key] where key is element of set, "difference"
            difference=sorted(list(difference))
            # sorting is necessary, so the date-time of the message is sorted
            #sorting creates a list with first old messages - then new messages
            #print(difference)
            
            #print these messages in the gui
            for ii in range(len(difference)):
                message_chiffre=self.server_content["message"][UserID_alice][difference[ii]]["message"]
                message_privkey=self.key_alice[1]
                print("chiffre", message_chiffre)
                #Decrypt message
                
                message_decryp=Crypto_method.Decrypt("rsa",message_chiffre,message_privkey)
                
                #print(message)
                self.input_make_bob(message_decryp,UserID_alice,list_UserIDs_bob[i],difference[ii])
                
        
        #Write a function to print the messages in specific window- not all of them in the same
        
        #create a loop with after-mehtod running alongiside with the other mysterious
        #tkinter loop(s) nowbody knows about
        
        #change this (milliseconds) if update is to slow- however performance might increase
        chat_update_period=2000
        
        self.init.after(chat_update_period, lambda: self.chat_update(UserID_alice,list_UserIDs_bob))
        
        
        #lambda is magic- without tkinter does shit

    def input_make_alice(self,message,UserID_alice,UserID_bob):
        #prints the message "message" from User "namevar" to the gui
        #if send==True the message is printed to the server
        message_print='\n'+UserID_alice+">> "+message
        message_store=UserID_alice +">> "+message
        nowtimedate=str(datetime.datetime.now())
        
        self.iot.insert(tk.END,message_print)
        self.chat_buffer[UserID_bob].append([nowtimedate,message_print])
        self.input_send(message,UserID_alice,UserID_bob,nowtimedate)
        USRdata.storeMessage(UserID_alice,UserID_bob,message_store,nowtimedate)
    
    def input_make_bob(self,message,UserID_alice,UserID_bob,datetime):
        #prints the message "message" from User "UserID_bob" to the gui
        message_print='\n'+ UserID_bob +">> "+message
        message_store=UserID_bob +">> "+message
        
        self.chat_buffer[UserID_bob].append([datetime,message_print])
        USRdata.storeMessage(UserID_alice,UserID_bob,message_store,datetime)
        #it should just printout the message, if its one of the courrent chat partner 
        #(the current Listbox entry)
        if self.UserID_Bob==UserID_bob:
            self.iot.insert(tk.END,message_print)
            
        #finally store the time of the last server extraction from bob
        USRdata.store_lastTime(UserID_alice,UserID_bob,datetime)
        
    def input_send(self,message,UserID_alice,UserID_bob,nowtimedate):
        print(message)
        
        #for now keyID is constant later there should be a local database of keys created earilier in time
        # so in order to be able to decrypt messages from earlier time
        keyID_alice=1
        keyID_bob=1
        
        
        #Integrating encryption here:
        #get key from bob
        server_content=self.j.pull(UserID_bob)
        print(server_content)
        #maybe write a request-method in the MyHTTPRequestHandler in the server.py file, so in order to make this more efficient
        key_bob=server_content["mykey"]["publickey"]
        method_bob=server_content["mykey"]["method"]
        keyID_bob=server_content["mykey"]["keyID"]
        message_chiffre=Crypto_method.Encrypt(method_bob,message,key_bob)
        
        #create a new public key for alice
        method_alice="rsa"
        self.key_alice=Crypto_method.Keys(method_alice) ##alice public key
        
        
        data={'senderID': UserID_alice, 'receiverID': UserID_bob ,'publickeys': self.key_alice[0], 'keyID_alice': keyID_alice, 'keyID_bob': keyID_bob , "method": method_alice, 'message': message_chiffre, "nowtimedate":nowtimedate}
        self.j.push(UserID_alice,data,"POST")

    def input_get(self):
        #get input inserted in the editor at command "Enter Key" or Button
        message=self.message.get(1.0, tk.END)
        self.message.delete(1.0,tk.END)
        return message
        
    def grid_adjuste(self,x,rows,cols):
        #input a list of rows and cols
        #e.g. [[1,2],[1,10]], where 1 is the row 2 and 10 are the weights
        #adjust grid when resized
        #https://infohost.nmt.edu/tcc/help/pubs/tkinter/web/grid-config.html
        for i in range(len(rows)):
            x.grid_rowconfigure(rows[i][0], weight=rows[i][1])
        for i in range(len(cols)):
            x.grid_columnconfigure(cols[i][0], weight=cols[i][1])
    
    def login(self):
        
        
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
        button2=tk.Button(self.login_frame_foot,text='Create Account',command=lambda: self.login_make_account_data(),relief=self.buttonRelief,bg=self.buttonColor, font=self.buttonFont)
        
        GUImatrix.grid_vert([button,button2],1)
        
        hline2=tk.Canvas(self.login_win, height=10)
        hline2.create_line(20, 5, 500, 5)
           
        #----------------------------------------------------------------------
        #Put it together
        #----------------------------------------------------------------------
        
        GUImatrix.grid_hor([frm_h,frm_o,hline2,frm_f],1)
        
        self.login_win.mainloop()

    def login_make(self):
        usrname=self.login_usrname.get()
        password=self.login_password.get()
        self.login_check(usrname,password)
        if self.login_check_bool==True:
            self.login_win.destroy()
            #the following are IMPORTANT initalisations
            self.UserID_Alice=usrname
            self.pubkey_generate()
            self.home()
            #Note:
            #you are allowed to (create instance of class tk.Tk())
            #create instance, mainloop instance, create another instance, mainloop other instance
            #for some reason however
            #Create instance, Create another instance, create mainloop of instance, create mainloop of other instance
            #gives an exception error
        elif self.login_check_bool==False:
            ...
        
        
    def login_make_account_data(self):
        l4txt1="Reenter Password"
        l4 = tk.Message(self.login_frame_opt, width=1000, text=l4txt1)
        l4.grid(row=3,column=1,sticky="nsew")
        pswd2=tk.Entry(self.login_frame_opt,show='*')
        pswd2.grid(row=3,column=2,sticky="nsew")
        button3=tk.Button(self.login_frame_foot,text='Confirm Account',command=lambda: self.make_account_server() ,relief=self.buttonRelief,bg=self.buttonColor, font=self.buttonFont)
        button3.grid(row=1,column=2,sticky="nsew")
    
    def make_account_server(self):
        #input is string
        UserID_bob=self.login_usrname.get()
        dict_py={"UserID_bob": UserID_bob}
        dict_js=json.dumps(dict_py)
        exists=self.j.useroperation(UserID_bob, "FINDUSER")
        print(exists)
        if exists==False:
            #create an "account" - so a .json file on the server side
            self.j.useroperation(dict_js,"CREATEACCOUNT")
            self.login_make()
        
    
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
        #print(self.login_check_bool)
        #if 
        #check if passphrase is correct:
        #for the beginning the passphrase will just be the username
        #if 
    
    def input_userSwitch(self):
        #A function which switches the text window output by
        listbox_row=self.lst.curselection()[0]
        #print("listbox ", listbox_row)
        
        #current UserID of communication partner
        UserID_bob_curr=self.contacts[listbox_row]
        
        #delete contents of Textbox
        self.iot.delete('1.0', tk.END)
        
        #print buffered messages of user: User_ID_bob_curr
        buffer=self.chat_buffer[UserID_bob_curr]
        if buffer !=[]:
            for i in range(len(buffer)):
                self.iot.insert(tk.END,buffer[i][1])
            
        
        #Set self.UserID_Bob
        self.UserID_Bob=UserID_bob_curr

    def home(self):
        
        
        #list of contacts of user
        self.contacts=list(self.j.pull(self.UserID_Alice)["message"].keys())
        
        #initialise chat - get from server
        self.chat_update_init(self.UserID_Alice,self.contacts)
        
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
        self.menubar()
        
        #----------------------------------------------------------------------
        #paned 1'st order
        #----------------------------------------------------------------------
        
        self.home_paned=tk.PanedWindow(self.init,bd=10)
        self.home_paned.configure(bg=self.bg)
        self.home_paned.pack(fill="both", expand=True)
        
        
        
        self.home_frame1=tk.Frame(self.init)
        #self.home_frame1.grid(row=1,column=1,sticky="nsew")
        self.home_frame2=tk.Frame(self.init)
        #self.home_frame2.grid(row=1,column=2,sticky="nsew")
        
        #----------------------------------------------------------------------
        #paned 2'nd order
        #----------------------------------------------------------------------
        
        self.home_subpaned=tk.PanedWindow(self.home_frame2,orient="vertical")
        self.home_subpaned.configure(bg=self.bg)
        self.home_subpaned.pack(fill="both", expand=True)
        

        self.home_subframe2_1=tk.Frame(self.home_frame2)
        #self.home_frame1.grid(row=1,column=1,sticky="nsew")
        self.home_subframe2_2=tk.Frame(self.home_frame2)
        #self.home_frame2.grid(row=1,column=2,sticky="nsew")
                
        #----------------------------------------------------------------------
        #chat list
        #----------------------------------------------------------------------
        
        self.lst = tk.Listbox(self.home_frame1)
        self.lst.bind('<<ListboxSelect>>',lambda x: self.input_userSwitch())
        #don't ask me why but here you will need an "x" after lambda and
        #before ":"
        #https://stackoverflow.com/questions/16215045/typeerror-lambda-takes-no-arguments-1-given
        
        self.lst.grid(row=1,column=1,sticky="nsew")
        #get json file contacts and insert contents here: example:
        for x in range(len(self.contacts)):
            self.lst.insert(tk.END,self.contacts[x])
        
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
        #scrollbar
        #----------------------------------------------------------------------
        
        self.home_scrollbar=tk.Scrollbar(self.home_subframe2_1, orient=tk.VERTICAL, command=self.iot.yview, width=15)
        self.home_scrollbar.grid(row=1,column=2,sticky="nsew")
        self.iot['yscrollcommand']=self.home_scrollbar.set
        
        #----------------------------------------------------------------------
        #input window
        #----------------------------------------------------------------------
        
        self.message=tk.Text(self.home_subframe2_2, height=4)
        self.message.grid(row=1,column=1,sticky="nsew")
        
        #----------------------------------------------------------------------
        #scrollbar
        #----------------------------------------------------------------------
        
        self.home_scrollbar_mes=tk.Scrollbar(self.home_subframe2_2, orient=tk.VERTICAL, command=self.message.yview, width=15)
        self.home_scrollbar_mes.grid(row=1,column=2,sticky="nsew")
        self.message['yscrollcommand']=self.home_scrollbar_mes.set
        
        #----------------------------------------------------------------------
        #adjust the grid
        #----------------------------------------------------------------------
        
        #self.grid_adjuste(self.init,[[1,1]],[[1,1],[2,10]])
        self.grid_adjuste(self.home_frame1,[[1,1],[2,0]],[[1,1]])
        self.grid_adjuste(self.home_subframe2_1,[[1,1]],[[1,1],[2,0]])
        self.grid_adjuste(self.home_subframe2_2,[[1,1]],[[1,1],[2,0]])
        
        #----------------------------------------------------------------------
        #Put it together
        #----------------------------------------------------------------------
        
        self.home_paned.add(self.home_frame1,sticky="nsew",stretch="always")
        self.home_paned.add(self.home_frame2,sticky="nsew")
        
        self.home_subpaned.add(self.home_subframe2_1,sticky="nsew",stretch="always")
        self.home_subpaned.add(self.home_subframe2_2,sticky="nsew")
        
        self.chat_update(self.UserID_Alice,self.contacts)
                
        self.end()
      
        

    def menubar(self):
        menubar=tk.Menu(self.init)
        filemenu=tk.Menu(menubar,tearoff=0)
        menubar.add_cascade(label='File',menu=filemenu)
        filemenu.add_command(label='Quit',command=self.init.quit)
        helpmenu=tk.Menu(menubar,tearoff=0)
        menubar.add_cascade(label='Help',menu=helpmenu)
        helpmenu.add_command(label='About',command=lambda: self.men_about())
        helpmenu.add_command(label='Help',command= lambda: self.men_help())
        configure=tk.Menu(menubar,tearoff=0)
        menubar.add_cascade(label='Config',menu=configure)
        configure.add_command(label='Add contact',command=lambda: self.men_addcontact())
        configure.add_command(label='Chats',command=self.init.quit)
        configure.add_command(label='change default server',command=lambda: self.men_serverconf())
        configure.add_command(label='Encryption Algorithm',command= lambda: self.men_encryptconf())
        self.init.config(menu=menubar)
        
    def men_help(self):
        men=tk.Tk()
        men.title("Cryptograph-Help")
        men.resizable(width=False, height=False)
        text1='Cryptograph-Helppage:'
        text2='The help documentation can be found at:'
        text3='https://homepage.univie.ac.at/stephanb15/Applications/Cryptograph/documentation.html'
        self.grid_adjuste(self.init,[[1,1]],[[1,1]])
        msg1 = tk.Message(men,width=1000, text=text1)
        msg2 = tk.Message(men,width=1000, text=text2)
        msg3 = tk.Message(men,width=1000, text=text3)
        msg1.config(font=self.headFont)
        
        GUImatrix.grid_hor([msg1,msg2,msg3],1)
        
        men.mainloop()
        
    def men_about(self):
        men=tk.Tk()
        #men.geometry("500x500")
        men.title("Cryptograph-About")
        men.resizable(width=False, height=False)
        self.grid_adjuste(self.init,[[1,1]],[[1,1]])
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
        l1.config(font=self.headFont)
        l3.config(font=('times',12, 'bold'))
        
        GUImatrix.grid_hor([l1,l2,l3,l4],1)
        
        men.mainloop()
        
    def men_addcontact(self):
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
        button=tk.Button(men,text='Find user', command= lambda: self.men_addcontact_server(usrname.get()))
        l1.config(font=self.headFont)
        
        GUImatrix.grid_hor([l1,hline,l2,hline2,usrname,button,l3],1)
        
        #Write some input box add contact and a button 
        #if contact exists add the contact- else print: contact doesn't exists
        #if wrinting it advanced use some search function
        men.mainloop()
        
    def men_addcontact_server(self,UserID_bob):
        #write serverrequest to add user to account (.json file)
        ...
        
    
    def men_serverconf(self):
        men=tk.Tk()
        men.title("Cryptograph-Change Default server")
        men.resizable(width=False, height=False)
        l1txt1 ='Insert http address here'
        l1 = tk.Message(men, width=1000, text=l1txt1)
        address=tk.Entry(men)
        button=tk.Button(men,text='Configure server')#, command= lambda: self.input_get())
        l1.config(font=self.headFont)
        
        GUImatrix.grid_hor([l1,address,button],1)
        
        men.mainloop()
        
    def men_encryptconf(self):
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
        l2txt1 ='Insert Algorithm expenation here'
        l3txt1 ='(See the help menue)'
        l1 = tk.Message(men, width=1000, text=l1txt1)
        l2 = tk.Message(men, width=1000, text=l2txt1)
        l3 = tk.Message(men, width=1000, text=l3txt1)
        encryptcode=tk.Entry(men)
        button=tk.Button(men,text='Configure server')#, command= lambda: self.input_get())
        l1.config(font=self.headFont)
        l1.grid(row=1,column=1,sticky="nsew")
        l2.grid(row=2,column=1,sticky="nsew")
        l3.grid(row=3,column=1,sticky="nsew")
        encryptcode.grid(row=4,column=1,sticky="nsew")
        button.grid(row=5,column=1,sticky="nsew")
        men.mainloop()

    def end(self):
        self.init.mainloop()

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
            print("Server Communication Error")
        
    def useroperation(self,UserID_bob,method):
        #pushed = urllib.request.Request(url=pathHome, data=data,method="FINDUSER")
        client2=http.client.HTTPConnection(self.serveradressHome,port=self.PortHome)
        client2.request(method=method,body=UserID_bob,url="")
        exists2="0"
        try:
            #this is a foolish work around but ive got no idea how to solve this else
            #https://stackoverflow.com/questions/4308182/getting-the-exception-value-in-python
            #https://stackoverflow.com/questions/27619258/httplib-badstatusline
            #the reason for this error arriving is that i might not adapt to http standard accordnig to forums, source
            instance=client2.getresponse()
            instance.read()
        except http.client.BadStatusLine as exists:
            exists2=str(exists)
        exists3=bool(int(exists2))
        return exists3
    
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
            keys=RSA.Keys_auto()
        
        return keys
            
    def Encrypt(method_str, message_str, pubkey):
        # I don't use self here, becouse i don't like to restrict the application of this class function 
        # I use strings as input output bexouse some cry ptographic methodes other than rsa
        # don't have numeric chiffre (i.e Substitution, Transopostion)
        
        if method_str== "rsa":
            message_numb=Crypto_method.Assign_number(message_str)
            print("mes", message_numb)
            chiffre=RSA.Encrypt_large(message_numb, pubkey, 24) #the length 19 should be made variable in the future
        else:
            #if the method is incorrect/ not given, there will be an identity en/decryption-
            message_str=chiffre
        return chiffre
        
    def Decrypt(method_str,chiffre,privkey):
        # I don't use self here, becouse i don't like to restrict the application of this class function
        if method_str== "rsa":
            message_str=RSA.Decrypt_large(chiffre, privkey,24)

            message_str=Crypto_method.Assign_charlst(message_str)
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
        print(os.urandom(k0))

##############################################################################
#                             Main
##############################################################################

gui=GUI()


##############################################################################
#                             Testing
##############################################################################

###Testing Encryption

mykeys=RSA.Keys_auto()#823,827)
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
message="12str_%&/§f 劒 ▦ ꉨ Ꞥ ꡁ ∉3"
keys=Crypto_method.Keys("rsa")
chiffre=Crypto_method.Encrypt("rsa",message,keys[0])
decryp=Crypto_method.Decrypt("rsa",chiffre,keys[1])
print(decryp)


j=ioserver("178.191.88.79","8000")
print(j.useroperation("Mustermann","FINDUSER"))

#print(hex(int(Crypto_method.Assign_number("Some normal length of a message- i might must compress this fomat somehow"))))
#d=Decrypt(mysterytext)
#readblmess=d.RSA(mykeys[1])
#print(readblmess)

#Testing Json


#output=j.pull("plain")
#print(output)

#output["message"]["Bob1"]="hAllO wORld"

