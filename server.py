import sys
import threading
from socket import *

host = '127.0.0.1'

if len(sys.argv) < 2:
    print("Please enter port number")
    exit()

port = int(sys.argv[1])

server = socket(AF_INET, SOCK_STREAM)
server.bind((host, port))

server.listen(10)

#Storing client names and connections in the lists
clients = []
username = []

#Send message recieved from a user to all users
def broadcast(message):
    for client in clients:
        client.send(message)

#It recieves messages from the clients. This functin is driven by the threads
#From each thread message is recieved and send to broadcast function to send it all the users
#If exception occures the function will close the client connection and removes client from client list

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            user = username[index]
            message = '< {} > left the chatroom'.format(user.encode())
            broadcast(message.encode())
            break

#This primary function first recieves messages from new users
#First it will take username from the client and appent it to the username and client list
#It send hello message to the client and activates its thread    
def reciev_messages():
    while True:
        client, addr = server.accept()
        print("Connected with {}".format(str(addr)))
        user = client.recv(1024).decode()
        username.append(user)
        clients.append(client)

        print("{} joined the chatroom".format(user))
        message = 'Hello ' + str(user)
        client.send(message.encode())

        thread = threading.Thread(target = handle_client, args = (client, ))
        thread.start()

print("Server is ready to recieve messages")
reciev_messages()


print("Closing server")
server.close()