import random
from math import ceil

class Transposition:
    
    def __init__(self):
        
        self.key = random.randint(3,3)
    
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
            
        
        
    
a = Transposition()

b = a.encrypt_Message("Hallo")
print(b)
print(a.decrypt_Message(b))
