#L

import numpy as np
import random
from math import ceil
import tkinter as tk
from tkinter import messagebox

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
            
            accurate_List = [((rows - i) * columns - 1) % (rows * columns) for i in range(columns*rows - len(message))]
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
    
def command(sub,trans,plain):
    
    allowed = [".",",","!","?"," "]
    for x in range(65,91):
        allowed.append(chr(x))
    for x in range(97,123):
        allowed.append(chr(x))  
    
    for c in plain:
        if c not in allowed:
            messagebox.showwarning("Achtung", "Datei enthält unbekannte Zeichen!\nEingabevorschrift beachten!")
            break
        
    sublist = [Substitution() for x in range(int(sub))]
    translist = [Transposition() for x in range(int(trans))]
    composition = list(set(sublist) | set(translist))
    ciphertext = plain

    random.shuffle(composition)

    for obj in composition:
        ciphertext = obj.encrypt_Message(ciphertext)

    composition = composition[::-1]

    plaintext = ciphertext

    for obj in composition:
        plaintext = obj.decrypt_Message(plaintext)

    output_Window = tk.Tk() 
    label = tk.Label(output_Window, text = "Verschlüsselte Nachricht : " + str(ciphertext) + "\nEntschlüsselte Nachtricht : " + str(plaintext))
    label.grid(row = 0, column = 0) 
    output_Window.mainloop()    

input_Window = tk.Tk()
input_Window.title("Composition")

blabel = tk.Label(input_Window, text = "Wieviele Substitutionschiffren sollen erstellt werden?")
blabel.grid(row = 0, column = 0)
sub = tk.Entry(input_Window)
sub.grid(row = 0, column = 1)
    
blabel = tk.Label(input_Window, text = "Wieviele Translationschiffren sollen erstellt werden?")
blabel.grid(row = 1, column = 0)
trans = tk.Entry(input_Window)
trans.grid(row = 1, column = 1)
    
blabel = tk.Label(input_Window, text = "Welcher Text soll verschlüsselt werden?\nBitte nur Buchstaben des neues englischen Alphabets eingeben!")
blabel.grid(row = 2, column = 0)
plain = tk.Entry(input_Window)
plain.grid(row = 2, column = 1)

button = tk.Button(input_Window, text =  "Verschlüsseln", command = lambda : command(sub.get(), trans.get(), plain.get()))
button.grid(row = 3,columnspan = 2)

input_Window.mainloop()
