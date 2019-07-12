#!/usr/bin/env python3
#This file is created by author: Stephan Bornberg
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 15:06:57 2019

@author: stephan
"""

#from lib.cryptoMath import crymath
#<--this for some reason doesn't work inside the lib directory
import lib.cryptoMath

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
        d=lib.cryptoMath.crymath.extndEuclid(e,phin)[1]
        #Find a representant inside the proper borders
        d=lib.cryptoMath.crymath.findrepres(d,phin,phin,1)
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
        #print(message_blocks)
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
            #print("str1",message_str)
            message_str=len_zero_block*"0"+message_str
            #print("str2",message_str)
            message_plain+=message_str
        return message_plain

