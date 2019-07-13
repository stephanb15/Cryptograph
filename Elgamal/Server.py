# Lanser Jakob

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from random import randint

class User:
    
    def __init__(self):
        
        self.name = ""
        self.private_Key = randint(2,5)
        self.public_Cyclic = None
        self.public_Key = None
        self.public_Exponent = None
        self.full_Key = 1
        
    def set_Name(self,name):
        
        self.name = name
        
    def set_Cyclic(self,cyclic):
        
        self.public_Cyclic = cyclic
        
    def set_Public_Key(self,key):
        
        self.public_Key = key
        
    def generate_Keys(self):
        
        self.public_Exponent = pow(self.public_Key,self.private_Key, self.public_Cyclic)
                                  
    def get_Exponent(self):
        
        return self.public_Exponent
    
    def get_Name(self):
        
        return self.name
    
    def calculate_Full_Key(self, friend_Exponent):
        
        while self.full_Key == 1:
            self.full_Key = pow(friend_Exponent, self.private_Key, self.public_Cyclic)
                                  
      
    def encrypt_Message(self,message):
        
        encrypted_Message = [chr((ord(message[i]) * self.full_Key)) for i in range(len(message))]
        return "".join(encrypted_Message)
    
    def decrypt_Message(self,message):
        
        decrypted_Message = [chr((int(ord(message[i]) / self.full_Key))) for i in range(len(message))]
        return "".join(decrypted_Message)

def accept_Clients():
    
    while True:
        client, client_address = SERVER.accept()
        print("IP: {0} PORT: {1} ist verbunden.".format(client_address[0], client_address[1]))
        client.send(bytes("Verbindung hergestellt. Bitte Usernamen wählen.", "utf8"))     
        if len(clients) == 0 :
            client.send(bytes("Gesprächspartner noch nicht verbunden.", "utf8"))
        addresses[client] = client_address
        Thread(target = handle_Clients, args=(client,)).start()


def handle_Clients(client):

    user = User()
    user.set_Name(client.recv(BUFSIZ).decode("utf8"))
    name = user.get_Name()    
    welcome = 'Hallo {0}! Zum chatten Nachricht in die Chatbox eingeben und auf \"Nachricht senden\" drücken.\nUm den Chatraum zu verlassen \"Over and out.\" schreiben.'.format(name)
    client.send(bytes(welcome, "utf8"))
    message = "{0} ist dem Raum beigetreten.".format(name)
    user.set_Cyclic(17)
    user.set_Public_Key(2)
    user.generate_Keys()
    print(clients)
    if len(clients) == 2:
        message = "Verbindung nicht sicher, Nachrichten werden verschlüsselt."        
    broadcast(user, bytes(message, "utf8"))
    clients[client] = user

    if len(clients) == 2 :
        for client in clients:
            for clientt in clients:
                if clients[client] != clients[clientt]:
                    clients[client].calculate_Full_Key(clients[clientt].get_Exponent())

    while True:
        message = client.recv(BUFSIZ)
        message = message.decode("utf8")
        message = user.encrypt_Message(message)
        message = bytes(message,"utf8")
        if message != bytes("Over and out.", "utf8"):           
            broadcast(user, message, name + ": ")
        else:
            client.send(bytes("Over and out.", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("{0} hat die Verbindung beendet.".format(name), "utf8"))
            break


def broadcast(user, message, prefix=""):
    
    if len(clients) < 3:
        message = message.decode("utf8")
        message = user.decrypt_Message(message)
        message = bytes(message, "utf8")
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + message)

        
clients = {}
addresses = {}

HOST = "127.0.0.1"
PORT = 10000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen()
    print("Warten auf Teilnehmer.")
    ACCEPT_THREAD = Thread(target = accept_Clients)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
SERVER.close()
