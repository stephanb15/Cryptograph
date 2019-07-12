
#This file is created by author: Jakob Lanser
import random

class Substitution:
    
    def __init__(self):
        
        self.alphabet = [".",",","!","?"," "]
        for x in range(65,91):
            self.alphabet.append(chr(x))
        for x in range(97,123):
            self.alphabet.append(chr(x))
        
        self.subAlphabet = [".",",","!","?"," "]
        for x in range(65,91):
            self.subAlphabet.append(chr(x))
        for x in range(97,123):
            self.subAlphabet.append(chr(x))  
        random.shuffle(self.subAlphabet)
    
    def encrypt_Message(self,message):
        
        encryptedMessage = ""
        for c in message:
            i = self.alphabet.index(c)
            c = self.subAlphabet[i]
            encryptedMessage += c
        return encryptedMessage
    
    def decrypt_Message(self,message):
        
        decryptedMessage = ""
        for c in message:
            i = self.subAlphabet.index(c)
            c = self.alphabet[i]
            decryptedMessage += c
            return decryptedMessage
