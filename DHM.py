import numpy as np

generator = 2
prime = 439351292910452432574786963588089477522344199

class User:
    def __init__(self, generator, prime):
        self.generator = generator
        self.prime = prime
        self.identity = np.random.random_integers(1,prime)
        self.fullKey = None
        
    def generateKeySender(self):
        key = self.generator**self.identity
        key = key%self.prime
        return key
    
    def generateKeyRecipient(self, receivedKey):
        fullKey = receivedKey**self.identity
        fullKey = fullKey%self.prime
        self.fullKey = fullKey
        return fullKey
    
    def encryptMessage(self, message):
        encryptedMessage = ""
        key = self.fullKey
        for c in message:
            encryptedMessage += chr(ord(c)+key)
        return encryptedMessage
    
    def decryptMessage(self, encryptedMessage):
        decryptedMessage = ""
        key = self.fullKey
        for c in encryptedMessage:
            decryptedMessage += chr(ord(c)-key)
        return decryptedMessage
