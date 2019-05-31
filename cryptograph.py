import math
import tkinter as tk
import numpy as np
import json
import urllib.request
import requests


namevar="plain"


##############################################################################
#                             GUI
##############################################################################

class GUI:
    def __init__(self):
        
        gui.login()
        
        #font for headings:
        self.headfont=('times',14, 'bold')
        
    def chat_update_init(self, UserID_alice,UserID_bob):
        
        #get all server contents from Bob
        self.server_content=j.pull(UserID_bob)
        
        #sieve messages dedicated to Alice 
        self.oldset=set(self.server_content["message"][UserID_alice].keys())
        
        #print chat history
        ##
        #
        ##
        
        #get all contents (messages, contacts from server as initialised)
        #maybe for performance create a synchronisation algorithms to
        #save from big downloads, later
        
        
    def chat_update(self,UserID_alice, UserID_bob):
        #write a function creating a list contaning all messenge keys "
        # i.e "2019-05-29 18:30:59.099567" 
        #after every server_update compare those lists
        #and if the list is alterd, print the contents to the gui 
        #of the matheamtical complement (set difference) of the old set to the new list
        
        #essential, as otherwise messanges no messages would income
        self.server_content=j.pull(UserID_bob) ######## CHANGE PLAIN TO GENERAL USERID
        
        self.newset=set(self.server_content["message"][UserID_alice].keys())
        #print(self.newset)
        difference=self.newset-self.oldset
        self.oldset=self.newset
        
        #order the differnce-set by date and print out the dedicated messages
        #, so the dictionary[key] where key is element of set, "difference"
        difference=sorted(list(difference))
        # sorting is necessary, so the date-time of the message is sorted
        #sorting creates a list with first old messages - then new messages
        print(difference)
        
        #print these messages in the gui
        for i in range(len(difference)):
            message=self.server_content["message"][UserID_alice][difference[i]]["message"]
            print(message)
            self.input_make_bob(message,UserID_bob)
        
        #Write a function to print the messages in specific window- not all of them in the same
        
        #create a loop with after-mehtod running alongiside with the other mysterious
        #tkinter loop(s) nowbody knows about
        
        #change this (milliseconds) if update is to slow- however performance might increase
        chat_update_period=2000
        
        self.init.after(chat_update_period, lambda: self.chat_update(UserID_alice,UserID_bob))
        
        
        #lambda is magic- without tkinter does shit

    def input_make_alice(self,message,UserID_alice,UserID_bob):
        #prints the message "message" from User "namevar" to the gui
        #if send==True the message is printed to the server
        
        self.iot.insert(tk.END,'\n'+UserID_alice+">> "+message)
        self.input_send(message,UserID_alice,UserID_bob)
        #Create command line
    
    def input_make_bob(self,message,UserID_bob):
        #prints the message "message" from User "namevar" to the gui
        #if send==True the message is printed to the server
        
        self.iot.insert(tk.END,'\n'+UserID_bob+">> "+message)
        
    def input_send(self,message,UserID_alice,UserID_bob):
        print(message)
        j=ioserver("http://188.23.146.121","8000")
        method="aeion"
        key="aefaef"
        data={'senderID': UserID_alice, 'receiverID': UserID_bob ,'publickeys': key, 'message': message}
        j.push(UserID_alice,data)

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
        l1txt1 ='Login'
        l2txt1='username:'
        l3txt1='password:'
        l1 = tk.Message(self.login_win, width=1000, text=l1txt1)
        l2 = tk.Message(self.login_win, width=1000, text=l2txt1)
        l3 = tk.Message(self.login_win, width=1000, text=l3txt1)
        self.login_usrname=tk.Entry(self.login_win)
        self.login_password=tk.Entry(self.login_win,show='*')
        
        #initialise check variable for login
        self.login_check_bool=False
        button=tk.Button(self.login_win,text='Make Login',command=lambda: self.login_make())
        l1.config(font=self.headfont)
        l1.grid(row=1,column=1,sticky="nsew")
        l2.grid(row=2,column=1,sticky="nsew")
        l3.grid(row=3,column=1,sticky="nsew")
        self.login_usrname.grid(row=2,column=2,sticky="nsew")
        self.login_password.grid(row=3,column=2,sticky="nsew")
        button.grid(row=5,column=2,sticky="nsew")
            
        self.login_win.mainloop()

    def login_make(self):
        usrname=self.login_usrname.get()
        password=self.login_password.get()
        self.login_check(usrname,password)
        if self.login_check_bool==True:
            self.login_win.destroy()
            self.home()
        elif self.login_check_bool==False:
            ...

                
    def login_check(self,username, passphrase):
        #checks if the login makes sence /is correct
        #check if username exists:
        adress=j.ip_adress_format()+username +".json"
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
        
    
    def home(self):
        
        UserID_alice=namevar
        UserID_bob="stephanb15"
        
        #initialise chat - get from server
        self.chat_update_init("stephanb15","plain")
        
        #list of contacts of user
        self.contacts=list(j.pull(namevar)["message"].keys())
        
        
        
        #GUI
        
        home_root = tk.Tk()
        self.init=home_root
        
        self.init.title("Cryptograph")
        self.menubar()
        
        #Frames
        self.home_paned=tk.PanedWindow(self.init,bd=10)
        self.home_paned.pack(fill="both", expand=True)
                
        self.home_frame1=tk.Frame(self.init)
        #self.home_frame1.grid(row=1,column=1,sticky="nsew")
        self.home_frame2=tk.Frame(self.init)
        #self.home_frame2.grid(row=1,column=2,sticky="nsew")
        
        
        self.message=tk.Text(self.home_frame2, height=4)
        
        ###output input window
        self.message.grid(row=2,column=2,sticky="nsew")
        
        ###chat list
        self.lst = tk.Listbox(self.home_frame1)
        self.lst.grid(row=1,column=1,sticky="nsew")
        #get json file contacts and insert contents here: example:
        for x in range(len(self.contacts)):
            self.lst.insert(tk.END,self.contacts[x])
        
        ####button
        button=tk.Button(self.home_frame1,text='Encrypt/send Message', command= lambda: self.input_make_alice(self.input_get(),UserID_alice,UserID_bob)) # insert command=Encryptionfunction
        #the remainder code line works with "lamda" without it dosen't however I don't know why
        button.grid(row=2,column=1)
        
        ###output window
        self.iot=tk.Text(self.home_frame2,wrap=tk.WORD)
        self.iot.grid(row=1,column=2,sticky="nsew")
        
        ###scrollbar
        self.home_scrollbar=tk.Scrollbar(self.home_frame2, orient=tk.VERTICAL, command=self.iot.yview)
        self.home_scrollbar.grid(row=1,column=3,sticky="nsew")
        
        self.iot['yscrollcommand']=self.home_scrollbar.set
        
        ###scrollbar
        self.home_scrollbar_mes=tk.Scrollbar(self.home_frame2, orient=tk.VERTICAL, command=self.message.yview)
        self.home_scrollbar_mes.grid(row=2,column=3,sticky="nsew")
        
        self.message['yscrollcommand']=self.home_scrollbar_mes.set
        
        
        #adjust the grid
        #self.grid_adjuste(self.init,[[1,1]],[[1,1],[2,10]])
        self.grid_adjuste(self.home_frame1,[[1,1]],[[1,1]])
        self.grid_adjuste(self.home_frame2,[[1,1]],[[1,1],[2,1]])
        
        self.home_paned.add(self.home_frame1,sticky="nsew",stretch="always")
        self.home_paned.add(self.home_frame2,sticky="nsew")
        
        
        gui.chat_update("stephanb15","plain")
        
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
        guih=GUI(men)
        text1='Cryptograph-Helppage:'
        text2='The help documentation can be found at:'
        text3='https://homepage.univie.ac.at/stephanb15/Applications/Cryptograph/documentation.html'
        self.grid_adjuste(self.init,[[1,1]],[[1,1]])
        msg1 = tk.Message(men,width=1000, text=text1)
        msg2 = tk.Message(men,width=1000, text=text2)
        msg3 = tk.Message(men,width=1000, text=text3)
        msg1.config(font=self.headfont)
        msg1.grid(row=1,column=1,sticky="nsew")
        msg2.grid(row=2,column=1,sticky="nsew")
        msg3.grid(row=3,column=1,sticky="nsew")
        guih.end()
        
    def men_about(self):
        men=tk.Tk()
        #men.geometry("500x500")
        men.title("Cryptograph-About")
        men.resizable(width=False, height=False)
        guih=GUI(men)
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
        l1.config(font=self.headfont)
        l3.config(font=('times',12, 'bold'))
        l1.grid(row=1,column=1,sticky="nsew")
        l2.grid(row=2,column=1,sticky="nsew")
        l3.grid(row=3,column=1,sticky="nsew")
        l4.grid(row=4,column=1,sticky="nsew")
        guih.end()
        
    def men_addcontact(self):
        men=tk.Tk()
        men.title("Cryptograph-Add contact")
        men.resizable(width=False, height=False)
        guih=GUI(men)
        l1txt1 ='Add Contacts'
        l2txt1='Input an exististing username.'
        l2txt2='(If the username does not exists de Feedback dialog will print an error)'
        l3txt1='Feedback:'
        l1 = tk.Message(men, width=1000, text=l1txt1)
        l2 = tk.Message(men, width=1000, text=l2txt1+'\n'+l2txt2)
        l3 = tk.Message(men, width=1000, text=l3txt1)
        usrname=tk.Entry(men)
        button=tk.Button(men,text='Find user')#, command= lambda: self.input_get())
        l1.config(font=self.headfont)
        l1.grid(row=1,column=1,sticky="nsew")
        l2.grid(row=2,column=1,sticky="nsew")
        usrname.grid(row=3,column=1,sticky="nsew")
        button.grid(row=4,column=1,sticky="nsew")
        l3.grid(row=5,column=1,sticky="nsew")
        #Write some input box add contact and a button 
        #if contact exists add the contact- else print: contact doesn't exists
        #if wrinting it advanced use some search function
        guih.end()
    
    def men_serverconf(self):
        men=tk.Tk()
        men.title("Cryptograph-Server Configurations")
        guih=GUI(men)
        #Write some input box to add website containing ip adress
        #in my case https://homepage.univie.ac.at/stephanb15/Applications/Cryptograph/serverip.json
        #print error messages
        #if wrinting it advanced use some search function
        guih.end()
        
    def men_encryptconf(self):
        men=tk.Tk()
        men.title("Cryptograph-Server Configurations")
        guih=GUI(men)
        #choose boxes (these dots) where you can choose the algorithm
        guih.end()

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
        self.username="stephanb15"    
    
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
    
    def push(self,UserID_sender,data):
        #data must be an dictionary of 
        #the userID dedicated to you
        #create a json string from python dictionary
        data=json.dumps(data)
        #create byte data
        data=bytes(data,encoding='utf8')
        #print(data)
        pathHome=self.ip_adress_format()+UserID_sender +".json"
        pushed = urllib.request.Request(url=pathHome, data=data,method='POST')
        try:
            urllib.request.urlopen(pushed)
        except:
            #by that I prevent the error message
            #"raise RemoteDisconnected("Remote end closed connection withou"
            #aldough writing to the server now works without a client error 
            #this is a dirty solution
            print("Server Communication Error")
        #Push the pulblic Key, and messages to self.username
        #maybe try "pip install ssh" but i would not like to do it with that
        #requests.put(pathHome,data)

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


class Keys:
    def RSA(prime1,prime2):
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

class Encrypt:
    def __init__(self,x):
        #input is to be the data you like to encrypt
        if isinstance(x,float):
            self.float=x
        elif isinstance(x,int):
            self.int=x
        elif isinstance(x,str):
            self.str=x
        else:
            print("Your input",x,"is not understood by this class")
            print("    try a different data type")

    def RSA(self, pubkey):
        #input the RSA public key tupel "pubkey" 
        encryption=(self.int)**pubkey[0] % pubkey[1]
        return encryption

class Decrypt:
    def __init__(self,x):
        #input is to be the data which you like to decrypt
        if isinstance(x,float):
            self.float=x
        elif isinstance(x,int):
            self.int=x
        elif isinstance(x,str):
            self.str=x
        else:
            print("Your input",x,"is not understood by this class")
            print("    try a different data type")
    def RSA(self, privkey):
        #input the RSA public key tupel "pubkey" 
        decryption=fastexp((self.int),privkey[0]) % (privkey[1][0]*privkey[1][1])
        #decryption=self.int**privkey[0] % (privkey[1][0]*privkey[1][1])
        return decryption



##############################################################################
#                             Main
##############################################################################

j=ioserver("http://188.23.146.121","8000")

gui=GUI()


##############################################################################
#                             Testing
##############################################################################

###Testing Encryption
e=Encrypt(232342)
k=Keys

mykeys=k.RSA(823,827)
print(mykeys)

mysterytext=e.RSA(mykeys[0])
print(mysterytext)

d=Decrypt(mysterytext)
readblmess=d.RSA(mykeys[1])
print(readblmess)

#Testing Json


#output=j.pull("plain")
#print(output)

#output["message"]["Bob1"]="hAllO wORld"

