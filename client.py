import socket
import select
import errno

HEADER_LENGHT = 10
IP = "127.0.0.1"
PORT = 9999


my_username = input("Username : ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP,PORT))
client_socket.setblocking(False)

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGHT}}".encode('utf-8')
client_socket.send(username_header + username)

while True:
    message = input(f"{my_username} > ")
    
    if message:
        message = message.encode('uft-8')
        message_header = f"{len(message) :< {HEADER_LENGHT}}".encode('utf-8')
        client_socket.send(message_header + message)
        
    try:
        while True:
            username_header = client_socket.recv(HEADER_LENGHT)
            if not len(username_header):
                print("Verbindung zum Server wurde getrennt")
                sys.exit()
            username_lenght = int(username_lenght.decode('utf-8').strip())
            username = client_socket.recv(username_lenght).decode('utf-8')
            
            message_header = client_socket.recv(HEADER_LENGHT)
            message_lenght = int(message_header.decode('utf-8').strip())
            
            print(f"{username} > {message}")
            
    except IOERROR as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Nachricht konnte nicht gelesen werden', str(e))
            sys.exit()
        continue
            
    except Exception as e:
        print('Folgender Fehler wurde erkannt',str(e))
