import numpy as np

prime = 7
generator = 3

class User:
    
    def __init__(self):
        
        self.prime = prime
        self.generator = generator
        self.private_Key = np.random.randint(2,prime)
        self.public_Key = (generator**self.private_Key)%prime
    
    def get_Public_Key(self):
        return self.public_Key
    
    def encrypt_Message(self, message, key_Recipient):
        
        key_Recipient = key_Recipient
        key = (generator**self.private_Key)%prime
        key = (key**key_Recipient)%prime
        encrypted_Message = ""
        for c in message:
            encrypted_Message += chr(ord(c)*key)
        return encrypted_Message
        
    def decrypt_Message(self, encrypted_Message, key_Sender):
       
        key_Sender = key_Sender
        private_Key = self.private_Key
        key = (key_Sender**(1/private_Key))%prime
        decrypted_Message = ""
        for c in encrypted_Message:
            decrypted_Message += chr(int(ord(c)*key))
        return decrypted_Message
            
User = User()

a = User.get_Public_Key()

print(User.encrypt_Message("Hallo",a))

a = User.get_Public_Key()

print(User.decrypt_Message(User.encrypt_Message("Hallo",a),a))
