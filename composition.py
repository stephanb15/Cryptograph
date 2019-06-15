import numpy as np
import random
from math import ceil

class Transposition:
    
    def __init__(self):
        
        self.key = random.randint(2,5)

    def encrypt_Message(self,message):
        
        rows = self.key
        columns = int(ceil(len(message) / self.key))
        message_List = list(message)
        
        while len(message_List) != rows*columns:
            
            message_List.append("1")
            
        message = "".join(message_List)
        index_List = [i*columns for i in range(rows+1)]
        soon_To_Be_Matrix = [message[index_List[i]:index_List[i+1]] for i in range(len(index_List)-1)]
        matrix = np.zeros((rows,columns), dtype = str)

        for i in range(rows):
            
            soon_To_Be_Matrix[i] = list(soon_To_Be_Matrix[i])
            matrix[i] = soon_To_Be_Matrix[i]
            
        matrix = np.transpose(matrix)
        encrypted_Message = [c for l in matrix for c in l]
        encrypted_Message = list(filter(lambda x: x != "1", encrypted_Message))
        return "".join(encrypted_Message)
        
    def decrypt_Message(self,message):
        
        rows = int(ceil(len(message) / self.key))
        columns = self.key
        message_List = list(message)
        
        if len(message) != rows*columns:
            
            inaccurate_List = [i for i in range(columns*rows - len(message))]
            accurate_List = [(rows - i)*columns-1 for i in inaccurate_List]
            accurate_List.reverse()
            
            for i in accurate_List:
                
                message_List.insert(i,"1")
                
            message = "".join(message_List)
        index_List = [i*columns for i in range(rows+1)]
        soon_To_Be_Matrix = [message[index_List[i]:index_List[i+1]] for i in range(len(index_List)-1)]
        matrix = np.zeros((rows,columns), dtype = str)

        for i in range(rows):
            
            soon_To_Be_Matrix[i] = list(soon_To_Be_Matrix[i])
            matrix[i] = soon_To_Be_Matrix[i]
            
        matrix = np.transpose(matrix)
        decrypted_Message = [c for l in matrix for c in l]
        decrypted_Message = list(filter(lambda x: x != "1", decrypted_Message))
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
    plain = input("Welcher Text soll verschlüsselt werden?\nBitte nur Buchstaben des neuen englischen Alphabets eingeben!")
    
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

#passt
