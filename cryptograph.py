import tkinter as tk
import json
import urllib.request
import requests
import os
import math
import datetime
##############################################################################
#                             GUI
##############################################################################

class GUI:
    def __init__(self):
        
        self.j=ioserver("http://188.23.146.121","8000")
        
        #font for headings:
        self.bg="grey70"#"cadet blue"
        self.headFont=('times',14, 'bold')
        self.buttonFont=('times',14, 'italic')
        self.buttonColor="white smoke" #"LightSteelBlue3" #
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
        ##
        #
        ##
        
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
                
                mesage_decryp=Crypto_method.Decrypt("rsa",message_chiffre,message_privkey)
                
                message_print='\n'+ list_UserIDs_bob[i] +">> "+mesage_decryp
                self.chat_buffer[list_UserIDs_bob[i]].append([difference[ii],message_print])
                #print(message)
                self.input_make_bob(message_print,list_UserIDs_bob[i],difference[ii])
        
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
        self.iot.insert(tk.END,message_print)
        self.input_send(message,UserID_alice,UserID_bob)
        self.chat_buffer[UserID_bob].append(["",message_print])
    
    def input_make_bob(self,message_print,UserID_bob,datetime):
        #prints the message "message" from User "UserID_bob" to the gui
        if self.UserID_Bob==UserID_bob:
            self.iot.insert(tk.END,message_print)
        
    def input_send(self,message,UserID_alice,UserID_bob):
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
        
        
        nowtimedate=str(datetime.datetime.now())
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
        
        #Frame Head
        self.login_frame_head=tk.Frame(self.login_win,bd=10)
        frm_h=self.login_frame_head
        self.icon_img = tk.PhotoImage(file=self.icon_path)
        photo=tk.Label(frm_h, image = self.icon_img)
        photo.grid(row=1,column=2,sticky="nsew")
        l1txt1 ='Login'
        l1 = tk.Message(self.login_frame_head, width=1000, text=l1txt1)
        l1.grid(row=1,column=1,sticky="nsew")
        l1.config(font=self.headFont)
        
        #Frame Options
        frm_o=self.login_frame_opt=tk.Frame(self.login_win,bd=10)
        l2txt1='Username:'
        l3txt1='Password:'
        l2 = tk.Message(self.login_frame_opt, width=1000, text=l2txt1)
        l3 = tk.Message(self.login_frame_opt, width=1000, text=l3txt1)
        l2.grid(row=1,column=1,sticky="nsew")
        l3.grid(row=2,column=1,sticky="nsew")
        log=self.login_usrname=tk.Entry(self.login_frame_opt)
        pswd=self.login_password=tk.Entry(self.login_frame_opt,show='*')
        log.grid(row=1,column=2,sticky="nsew")
        pswd.grid(row=2,column=2,sticky="nsew")
        
        #Frame Foot
        frm_f=self.login_frame_foot=tk.Frame(self.login_win,bd=10)
        #initialise check variable for login
        self.login_check_bool=False
        button=tk.Button(self.login_frame_foot,text='Make Login',command=lambda: self.login_make(),relief="flat",bg=self.buttonColor, font=self.buttonFont)
        button.grid(row=1,column=1,sticky="nsew")
        
        #Put it together
        frm_h.grid(row=1,column=1,sticky="nsew")
        frm_o.grid(row=2,column=1,sticky="nsew")
        frm_f.grid(row=3,column=1,sticky="nsew")
        
        
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
        
        
        #GUI
        
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
        
        #paned 1'st order
        self.home_paned=tk.PanedWindow(self.init,bd=10)
        self.home_paned.configure(bg=self.bg)
        self.home_paned.pack(fill="both", expand=True)
        
        
        
        self.home_frame1=tk.Frame(self.init)
        #self.home_frame1.grid(row=1,column=1,sticky="nsew")
        self.home_frame2=tk.Frame(self.init)
        #self.home_frame2.grid(row=1,column=2,sticky="nsew")
        
        
        #paned 2'nd order
        self.home_subpaned=tk.PanedWindow(self.home_frame2,orient="vertical")
        self.home_subpaned.configure(bg=self.bg)
        self.home_subpaned.pack(fill="both", expand=True)
        

        self.home_subframe2_1=tk.Frame(self.home_frame2)
        #self.home_frame1.grid(row=1,column=1,sticky="nsew")
        self.home_subframe2_2=tk.Frame(self.home_frame2)
        #self.home_frame2.grid(row=1,column=2,sticky="nsew")
                
        
        ###chat list
        self.lst = tk.Listbox(self.home_frame1)
        self.lst.bind('<<ListboxSelect>>',lambda x: self.input_userSwitch())
        #don't ask me why but here you will need an "x" after lambda and
        #before ":"
        #https://stackoverflow.com/questions/16215045/typeerror-lambda-takes-no-arguments-1-given
        
        self.lst.grid(row=1,column=1,sticky="nsew")
        #get json file contacts and insert contents here: example:
        for x in range(len(self.contacts)):
            self.lst.insert(tk.END,self.contacts[x])
        

        
        ####button
        button=tk.Button(self.home_frame1,text='Encrypt/send Message ✍', command= lambda: self.input_make_alice(self.input_get(),self.UserID_Alice,self.UserID_Bob),bg=self.buttonColor ,relief="groove", font=self.buttonFont) # insert command=Encryptionfunction
        #used a unicode character for this:
        #https://unicode-table.com/en/270D/
        #the remainder code line works with "lamda" without it dosen't however I don't know why
        button.grid(row=2,column=1,sticky="nsew")
        
        
        ###output window
        self.iot=tk.Text(self.home_subframe2_1,wrap=tk.WORD)
        self.iot.grid(row=1,column=1,sticky="nsew")
        
        ###scrollbar
        self.home_scrollbar=tk.Scrollbar(self.home_subframe2_1, orient=tk.VERTICAL, command=self.iot.yview, width=15)
        self.home_scrollbar.grid(row=1,column=2,sticky="nsew")
        self.iot['yscrollcommand']=self.home_scrollbar.set
        
        
        ###input window
        self.message=tk.Text(self.home_subframe2_2, height=4)
        self.message.grid(row=1,column=1,sticky="nsew")
        
        ###scrollbar
        self.home_scrollbar_mes=tk.Scrollbar(self.home_subframe2_2, orient=tk.VERTICAL, command=self.message.yview, width=15)
        self.home_scrollbar_mes.grid(row=1,column=2,sticky="nsew")
        self.message['yscrollcommand']=self.home_scrollbar_mes.set
        
        
        #adjust the grid
        #self.grid_adjuste(self.init,[[1,1]],[[1,1],[2,10]])
        self.grid_adjuste(self.home_frame1,[[1,1],[2,0]],[[1,1]])
        self.grid_adjuste(self.home_subframe2_1,[[1,1]],[[1,1],[2,0]])
        self.grid_adjuste(self.home_subframe2_2,[[1,1]],[[1,1],[2,0]])
        
        
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
        msg1.grid(row=1,column=1,sticky="nsew")
        msg2.grid(row=2,column=1,sticky="nsew")
        msg3.grid(row=3,column=1,sticky="nsew")
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
        l1.grid(row=1,column=1,sticky="nsew")
        l2.grid(row=2,column=1,sticky="nsew")
        l3.grid(row=3,column=1,sticky="nsew")
        l4.grid(row=4,column=1,sticky="nsew")
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
        usrname=tk.Entry(men)
        button=tk.Button(men,text='Find user')#, command= lambda: self.input_get())
        l1.config(font=self.headFont)
        l1.grid(row=1,column=1,sticky="nsew")
        l2.grid(row=2,column=1,sticky="nsew")
        usrname.grid(row=3,column=1,sticky="nsew")
        button.grid(row=4,column=1,sticky="nsew")
        l3.grid(row=5,column=1,sticky="nsew")
        #Write some input box add contact and a button 
        #if contact exists add the contact- else print: contact doesn't exists
        #if wrinting it advanced use some search function
        men.mainloop()
    
    def men_serverconf(self):
        men=tk.Tk()
        men.title("Cryptograph-Change Default server")
        men.resizable(width=False, height=False)
        l1txt1 ='Insert http address here'
        l1 = tk.Message(men, width=1000, text=l1txt1)
        adress=tk.Entry(men)
        button=tk.Button(men,text='Configure server')#, command= lambda: self.input_get())
        l1.config(font=self.headFont)
        l1.grid(row=1,column=1,sticky="nsew")
        adress.grid(row=3,column=1,sticky="nsew")
        button.grid(row=4,column=1,sticky="nsew")
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
#                             Server
##############################################################################
       
class ioserver:
    def __init__(self,serveradressHome,PortHome):
        self.serveradressHome=serveradressHome
        self.PortHome=PortHome
        #for testing- use the localhost
        #self.serveradressHome="http://localhost:8000/"
    
    def ip_adress_format(self):
        path=self.serveradressHome+":"+self.PortHome+"/"
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
#                             Matheamtics
##############################################################################

def extndEuclid(a,b):
    rtupel=[a,b]
    stupel=[1,0]
    while not(rtupel[1]==0):
        q=rtupel[0]//rtupel[1]
        saveR=rtupel[1]
        rtupel[1]=rtupel[0]-q*rtupel[1]
        rtupel[0]=saveR
        
        saveS=stupel[1]
        stupel[1]=stupel[0]-stupel[1]*q
        stupel[0]=saveS
        #uncooment for tests
        #print(rtupel,stupel)
    
    return (rtupel[0],stupel[0])

def findrepres(rep,mod,bmax,bmin):
    #finds a representant "rep" of an equivalence class in certain borders
    #mathematically: trys to find a  $$ rep \in (bmin,bmax) $$
    #where the parantheses "(" and ")" indicate $$ bmin,bmax \notin (bmin,bmax) $$
    #thus indicate an open intervall
    #This function might loop infinitly if non proper borders are given
    if bmin>bmax:
        bmax,bmin=bmin,bmax
    if rep >= bmax:
        while rep>=bmax:
            rep=rep-mod
    if rep <= bmin:
        while rep<=bmin:
            rep=rep+mod
    #print("bmin",bmin,"bmax",bmax,"rep",rep,"mod",mod)
    return(rep)
    #Maybe write an error message when oscillation occurs:
    #Thus print a message when rep became >=bmax and later <=bmin
    #so then we know there is no such element $$ rep \in (bmin,bmax) $$
        
def fastexp(base,power):
    #A function to make fast product calculation a^n,
    #where a, n are integers in this implementation
    #this function unfortunately is quiet as fast as the pythons power **
    #so imporvison might be necessary if possible
    #print("power",power)
    if power<=0:
        #this schouldn't actually occure for the public key
        return base**power
    
    binpow_str=bin(power)
    #convert binary string to list of "0" and "1"s
    binpow_intarr=[]
    
    for i in range(2,len(binpow_str)):
        #print(binpow_str)
        binpow_intarr.append(int(binpow_str[i]))
    binpow_intarr=binpow_intarr[::-1]
    #iterativ fast expoential calculation
    result=1
    for i in range(len(binpow_intarr)):
        if binpow_intarr[i]==1:
            result*=base**(2**i)
    return result

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


class RSA:
    #static methodes are used in this class to prevent chaos
    #furthermore I don't like having to destroy a class after each instance creation
    
    def Keys(prime1,prime2):
        #find the keys for RSA encryption decryption
        n=prime1*prime2
        phin=(prime1-1)*(prime2-1)
        enorm=2**16+1
        #a usual value for the encryption exponent (performance)
        #e=23
        e=enorm
        if e > phin:
            print("Error: choose greater prime numbers")
            # or in case calculate a e <phin with gcd(e,phin)=1
            #which might either be a performance issue or a security issue
        #find a "d" with d*e kongurent 1 module phin
        public=(e,n)
        d=extndEuclid(e,phin)[1]
        #Find a representant inside the proper borders
        d=findrepres(d,phin,phin,1)
        private=(d,(prime1,prime2))
        return (public,private)
    
    def Keys_auto():
        #No primes must be given for this keygeneration
        #another function implemented later (a primefinder) will do that for you
        
        #for the beginning these primes will serve as dummy (later a primefinder will be put there instead)
        prime1=7337488745629403488410174275830423641502142554560856136484326749638755396267050319392266204256751706077766067020335998122952792559058552724477442839630133
        prime2=3125250912230709951372256510072774348164206451981118444862954305561681091773335180100000000000000000537
        
        return RSA.Keys(prime1,prime2)
        

    def Encrypt(message, pubkey):
        #input the RSA public key tupel "pubkey" 
        #encryption=(message)**pubkey[0] % pubkey[1]
        encryption=pow(message,pubkey[0],pubkey[1])
        return encryption
    
    def Encrypt_large(message_str, pubkey, blocklength):
        # A function encrypting messages larger than prime1*prime2 by building blocks
        
        #Creating Blocks
        maxindex=len(message_str)-1
        #indexl=math.ceil(len(message_str)/blocklength)
        
        #DEFINTION: of indexl
        #indexl:=max({0,blocklength, ...., n*blocklength}), such that n:=max({i; i*blocklength<=maxindex})
        #This is equivalent to 
        if len(message_str)>blocklength:
            indexl= len(message_str)-len(message_str)%blocklength
            #last index modulo blocklength of message_str
        else:
            indexl=0
        
        #DEFINTION: of indexll
        #indexll:=max({i; i*blocklength<=maxindex}\{n}), where n is defined aboth
        #this is equivalent to
        if indexl>blocklength:
            indexll=indexl-blocklength
            #last index modulo blocklength which is not indexl
        elif indexl==blocklength:
            #so as indexl=blocklength according to definition of indexl, indexll can either be equal 0 or equal blocklength 
            #so as indexll exculdes n "\{n}", it can just be equal 0
            indexll=0
        elif indexl<blocklength:
            #as indexl < blocklength undefined  as indexll=max{"empty set"} is undefined
            print("Undefined case: indexl < blocklength")
        
        
        #DEFINTION: of message_blocks
        message_blocks=[]
            
        
        if indexl>=blocklength:
            message_blocks.extend([int(message_str[blocklength*i:blocklength*(i+1)]) for i in range(int(indexll/blocklength)+1)])
        
        #The last block must have 0's trailing, else it's easy to construct an example where Decryption will make an error
        msg_end=message_str[indexl:maxindex+1]
        msg_end_len=len(msg_end)
        #add trailing zeros
        msg_end=msg_end+(blocklength-msg_end_len)*"0"
        message_blocks.extend([int(msg_end)])
        print(message_blocks)
        #proof that message is a contenation of the elements of message_blocks such that
        #message == message_blocks[0] || message_blocks[1] || ... || message_blocks[n],
        #where n is the maximal projection of list message_blocks
        #PROOF: 
        #if len(message_str) < blocklength
        #
        chiffrat_blocks=[]
        for i in range(len(message_blocks)):
            #contenate the encrypted blocks
            chiffrat_blocks.append(RSA.Encrypt(message_blocks[i], pubkey))
        return chiffrat_blocks
        
    def Decrypt(message, privkey):
        #input the RSA public key tupel "pubkey" 
        #decryption=fastexp((message),privkey[0]) % (privkey[1][0]*privkey[1][1])
        
        #the following python build in function is much faster in calculating the power modulo something
        decryption=pow(message,privkey[0],(privkey[1][0]*privkey[1][1]))
        
        #decryption=self.int**privkey[0] % (privkey[1][0]*privkey[1][1])
        return decryption
    
    def Decrypt_large(message_blocks, privkey, blocklength):
        message_plain=""
        for i in range(len(message_blocks)):
            #contenate the decrypted blocks
            #restore leading 0's eliminated by int() function in the Encrypt methode
            message_i=RSA.Decrypt(message_blocks[i], privkey)
            message_str=str(message_i)
            len_zero_block=blocklength-len(message_str)
            print("str1",message_str)
            message_str=len_zero_block*"0"+message_str
            print("str2",message_str)
            message_plain+=message_str
        return message_plain
    
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
#print(hex(int(Crypto_method.Assign_number("Some normal length of a message- i might must compress this fomat somehow"))))
#d=Decrypt(mysterytext)
#readblmess=d.RSA(mykeys[1])
#print(readblmess)

#Testing Json


#output=j.pull("plain")
#print(output)

#output["message"]["Bob1"]="hAllO wORld"

