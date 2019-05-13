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
        print(stupel,rtupel)
    
    return (rtupel,stupel)
    
print(extndEuclid(1234,10))


class Keys:
    def RSA(prime1,prime2):
        #find the keys for RSA encryption decryption
        n=prime1*prime2
        phin=(prime1-1)(prime2-1)
        enorm=2**16+1
        #a usual vale for the encryption exponent (performance)
        e=enorm
        if enorm > phin:
            print("Error: choose greater prime numbers")
            # or in case calculate a e <phin with gcd(e,phin)=1
            #which might either be a performacne issue or a security issue
        #find a "d" with d*e kongurent 1 module phin
        public=(e,n)
        private=d
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
        return self.int


x=Encrypt(11341)
print(x.RSA(11))
GUI()
