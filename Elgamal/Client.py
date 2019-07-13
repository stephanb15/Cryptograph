# Lanser Jakob

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk

def receive_Message():

    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            message_List.insert(tk.END, msg)
        except OSError:
            break

def send_Message():
    
    message = my_Message.get()
    my_Message.set("")
    client_socket.send(bytes(message, "utf8"))
    if message == "Over and out.":
        client_socket.close()
        top.quit()

def close():
    
    my_Message.set("Over and out.")
    send_Message()

top = tk.Tk()
top.title("Elgamal")

window = tk.Frame(top)
my_Message = tk.StringVar()

yscrollbar = tk.Scrollbar(window)
xscrollbar = tk.Scrollbar(window)
message_List = tk.Listbox(window, height = 25, width = 70, yscrollcommand = yscrollbar.set)
yscrollbar.pack(side = tk.RIGHT, fill = tk.Y)
yscrollbar.config(orient = tk.VERTICAL ,command = message_List.yview)
xscrollbar.pack(side = tk.BOTTOM, fill = tk.X)
xscrollbar.config(orient = tk.HORIZONTAL ,command = message_List.xview)
message_List.pack(side = tk.LEFT, fill = tk.BOTH)
message_List.pack()
window.pack()

entry_field = tk.Entry(top, textvariable = my_Message)
entry_field.bind("<Return>", send_Message)
entry_field.pack()
send_button = tk.Button(top, text = "Nachricht senden", command = send_Message)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", close)

HOST = "127.0.0.1"
PORT = 10000

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target = receive_Message)
receive_thread.start()
tk.mainloop()
