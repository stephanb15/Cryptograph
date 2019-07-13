#This file is created by author: Jakob Lanser
import random

class User:
    
    def __init__(self):
        
        self.private_Key = random.randint(2,5)
        self.public_Cyclic = None
        self.public_Key = None
        self.public_Exponent = None
        self.full_Key = None
    
    def set_Cyclic(self,cyclic):
        
        self.public_Cyclic = cyclic
        
    def set_Public_Key(self,key):
        
        self.public_Key = key
        
    def generate_Keys(self):
        
        self.public_Exponent = pow(self.public_Key,self.private_Key, self.public_Cyclic)
                                  
    def get_Exponent(self):
        
        return self.public_Exponent

    def calculate_Full_Key(self, friend_Exponent):
        
        self.full_Key = pow(friend_Exponent, self.private_Key, self.public_Cyclic)
                                  
      
    def encrypt_Message(self,message):
        
        encrypted_Message = [chr((ord(message[i]) * self.full_Key)) for i in range(len(message))]
        print(encrypted_Message)
        return "".join(encrypted_Message)
    
    def decrypt_Message(self,message):
        
        decrypted_Message = [chr((int(ord(message[i]) / self.full_Key))) for i in range(len(message))]
        print(decrypted_Message)
        return "".join(decrypted_Message)
    
    def test(self):    
        
        print(self.public_Cyclic)
        print(self.private_Key)
        print(self.public_Key)
        print(self.public_Exponent)
        print(self.full_Key)

        
#Simulation
a = User()
b = User()
a.set_Cyclic(17)
b.set_Cyclic(17)
a.set_Public_Key(2)
b.set_Public_Key(2)
a.generate_Keys()
b.generate_Keys()
a.calculate_Full_Key(b.get_Exponent())
b.calculate_Full_Key(a.get_Exponent())
aa = a.encrypt_Message("Ich hoffe, dass dieser Satz genau in dieser Form wiedergegeben wird.")
print(aa)
bb = b.decrypt_Message(aa)
print(bb)
a.test()
b.test()            
