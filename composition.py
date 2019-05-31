import random
from math import ceil

class Transposition:
    
    def __init__(self):
        
        self.key = random.randint(2,8)
    
    def encrypt_Message(self,message):
        
        encrypted_Message = [""]*self.key       
        for i in range(self.key):
            j = i           
            while j < len(message):                
                encrypted_Message[i] += message[j]               
                j += self.key
                
        return "".join(encrypted_Message)
    
    def decrypt_Message(self,message):
        
        decrypted_Message = [""]*int(ceil(len(message) / self.key))
        for i in range(int(ceil(len(message) / self.key))):
            j = i
            while j < len(message):
                decrypted_Message[i] += message[j]
                j += int(ceil(len(message) / self.key))
                
        return "".join(decrypted_Message)

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
    
def questionnaire():
    
    sub = input("Wieviele Substitutionschiffren sollen erstellt werden?")
    trans = input("Wieviele Translationschiffren sollen erstellt werden?")
    plain = input("Welcher Text soll verschlüsselt werden?\nBitte nur Buchstaben des neues englischen Alphabets eingeben!")
    
    return [sub,trans,plain]

sub,trans,plain = questionnaire()

sublist = [Substitution() for x in range(int(sub))]
translist = [Transposition() for x in range(int(trans))]
composition = list(set(sublist) | set(translist))

random.shuffle(composition)

for obj in composition:
    plain = obj.encrypt_Message(plain)
print(plain)

composition = composition[::-1]

for obj in composition:
    plain = obj.decrypt_Message(plain)
print(plain)

#Problem beim Entschlüsselungsprozess der Transpositionen
