import sys
import threading
from socket import *

host = '127.0.0.1'

if len(sys.argv) < 3:
    print("Please enter server port number and username respectively")
    sys.exit()

#Port number of the server as user input
port = int(sys.argv[1])

#Creating client socket and connecting it with server 
client = socket(AF_INET, SOCK_STREAM)
client.connect((host, port))

#Username from command line
user = str(sys.argv[2])

#Recieving messages from the server
def recieve_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            print(message)

        except:
            print("Error !!!!")
            client.close()
            break

#Get message from user and send to the server    
def write_message():
    while True:
        c_input = str(input())
        message = '< {} > {}'.format(user, c_input)
        client.send(message.encode())

#Sending first message with username to the server
client.send(user.encode())

print("Client is ready to send the message")

#Creating recieving thread to recieve messages from the server
recieve_thread = threading.Thread(target = recieve_messages)
recieve_thread.start()

#Creating writing thread to send the message to the server
write_thread = threading.Thread(target = write_message)
write_thread.start()

