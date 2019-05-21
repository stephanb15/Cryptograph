import math
import tkinter as tk
import numpy as np
import json
import urllib.request


namevar="Alice"
    

class GUI:
    def __init__(self, x):
        self.init=x
        listbox = tk.Listbox(self.init)
        self.lst=listbox
        iotext=tk.Text(self.init)
        self.iot=iotext
        self.iter=0
        
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
        
    def chatbox(self):
        self.iot.grid(row=1,column=2)
        
    def input_make(self,nameva):
        self.iot.insert(tk.END,'\n'+namevar+">>")
        #Create command line
        
    def chatlist(self):
        self.lst.grid(row=1,column=1,sticky="nsew")
        #get json file contacts and insert contents here: example:
        self.lst.insert(tk.END,"Bob1")
        
    def input_get(self):
        self.iter=self.iter+1
        #get input inserted in the editor at command "Enter Key" or Button 
        self.lst.get(self.iter)
        self.input_make(namevar)
        
    def button(self):
        button=tk.Button(self.init,text='Encrypt/send Message', command= lambda: self.input_get()) # insert command=Encryptionfunction
        #the remainder code line works with "lamda" without it dosen't however I don't know why
        button.grid(row=2,column=2)
        
    def men_help(self):
        helpmesg=tk.Tk()
        helpmesg.title("Cryptograph-Help")
        guih=GUI(helpmesg)
        guih.end()
        
    def men_about(self):
        helpmesg=tk.Tk()
        helpmesg.title("Cryptograph-About")
        guih=GUI(helpmesg)
        guih.end()
    
    def men_addcontact(self):
        helpmesg=tk.Tk()
        helpmesg.title("Cryptograph-Add contact")
        guih=GUI(helpmesg)
        #Write some input box add contact and a button 
        #if contact exists add the contact- else print: contact doesn't exists
        #if wrinting it advanced use some search function
        guih.end()
    
    def men_serverconf(self):
        helpmesg=tk.Tk()
        helpmesg.title("Cryptograph-Server Configurations")
        guih=GUI(helpmesg)
        #Write some input box to add website containing ip adress
        #in my case https://homepage.univie.ac.at/stephanb15/Applications/Cryptograph/serverip.json
        #print error messages
        #if wrinting it advanced use some search function
        guih.end()
        
    def men_encryptconf(self):
        helpmesg=tk.Tk()
        helpmesg.title("Cryptograph-Server Configurations")
        guih=GUI(helpmesg)
        #choose boxes (these dots) where you can choose the algorithm
        guih.end()

    def end(self):
        self.init.mainloop()
       
class json:
    def __init__(self):
        self.serveradress="https://www.unet.univie.ac.at/~stephanb15/Applications/Cryptograph/"
        self.username="stephanb15"

    def pull(self,UserID):
        #get the pulblic Key, messages from user :UserID
        #https://docs.python.org/3/howto/urllib2.html
        #https://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script
        with urllib.request.urlopen(self.serveradress+UserID +".json") as response:
            data=response.read().decode()
            #print(self.serveradress+UserID+".json")
            #print(data)
            
    def push(self):
        #Push the pulblic Key, and messages to self.username
        #maybe try "pip install ssh" but i would not like to do it with that
        ...

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

root = tk.Tk()
root.title("Cryptograph")
gui=GUI(root)
gui.button()
gui.menubar()
gui.chatbox()
gui.chatlist()
gui.input_get()
gui.end()

###Testing Encryption
e=Encrypt(2340)
k=Keys

mykeys=k.RSA(823,827)
print(mykeys)

mysterytext=e.RSA(mykeys[0])
print(mysterytext)

d=Decrypt(mysterytext)
readblmess=d.RSA(mykeys[1])
print(readblmess)

#Testing Json
j=json()
j.pull("plain")