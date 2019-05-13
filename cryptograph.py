import math
import tkinter as tk
import numpy as np

def GUI():
    root = tk.Tk()
    button=tk.Button(root,text='Encrypt/send Message') # insert command=Encryptionfunction
    button.grid(row=2,column=1)
    root.title("Cryptograph")
    iotext=tk.Text(root)
    iotext.grid(row=1,column=1)
    menubar=tk.Menu(root)
    filemenu=tk.Menu(menubar,tearoff=0)
    menubar.add_cascade(label='Datei',menu=filemenu)
    menubar.add_cascade(label='Help',menu=filemenu)
    filemenu.add_command(label='Beenden',command=root.quit)
    filemenu.add_command(label='Insert File',command=root.quit)
    root.config(menu=menubar)
    root.mainloop()


def extndEuclid(a,b):
    rtupel=[a,b]
    stupel=[1,0]
    while not(rtupel[0]==0 or rtupel[1]==0):
        q=rtupel[0]//rtupel[1]
        saveR=rtupel[1]
        rtupel[1]=rtupel[0]-q*rtupel[1]
        rtupel[0]=saveR
        
        saveS=stupel[1]
        stupel[1]=stupel[0]-stupel[1]*q
        stupel[0]=saveS
        #uncooment for tests
        print(rtupel,stupel)
    
    return (rtupel[0],stupel[0])

def fastexp(base,power):
    #A function to make fast product calculation a^n,
    #where a, n are integers in this implementation
    #this function unfortunately is quiet as fast as the pythons power **
    #so imporvison might be necessary if possible
    
    if power<=0:
        #this schouldn't actually occure for the public key
        return base**power
    
    binpow_str=bin(power)
    #convert binary string to list of "0" and "1"s
    binpow_intarr=[]
    
    for i in range(2,len(binpow_str)):
        print(binpow_str)
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
        #a usual vale for the encryption exponent (performance)
        e=3
        #e=enorm
        if e > phin:
            print("Error: choose greater prime numbers")
            # or in case calculate a e <phin with gcd(e,phin)=1
            #which might either be a performance issue or a security issue
        #find a "d" with d*e kongurent 1 module phin
        public=(e,n)
        d=extndEuclid(e,n)[1]
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
        return decryption

GUI()

###Testing functions
x=Encrypt(23)
y=Keys

mykeys=y.RSA(11,23)
print(mykeys)

mysterytext=x.RSA(mykeys[0])
print(mysterytext)

z=Decrypt(mysterytext)
readblmess=z.RSA(mykeys[1])
print(readblmess)


