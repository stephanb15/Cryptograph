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
        
    def getAlphabet(self):
        return self.alphabet

    def getSubAlphabet(self):
        return self.subAlphabet
    
    def encryptMessage(self,message):
        
        encryptedMessage = ""
        for c in message:
            i = self.alphabet.index(c)
            c = self.subAlphabet[i]
            encryptedMessage += c
        return encryptedMessage
    
    def decryptMessage(self,message):
        
        decryptedMessage = ""
        for c in message:
            i = self.subAlphabet.index(c)
            c = self.alphabet[i]
            decryptedMessage += c
        return decryptedMessage
        
a = Substitution()

print(a.getAlphabet())
print(a.getSubAlphabet())
b = a.encryptMessage("Hallo Welt!")
print(b)
print(a.decryptMessage(b))
