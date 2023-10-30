'Chat Room Connection - Client-To-Client'

import threading   #running several diff programs
import socket

host = '10.1.224.137' #localhost
#netstat
port = 49698
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  #s -> socket
server.bind((host,port))
server.listen()
clients = []
aliases = []

def broadcast(message):
    for client in clients:
        client.send(message)

# function to handle client's connection
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)  #max num of bytes server can recv from client
            broadcast(message)
            # print("### : ",(message.decode('utf-8')).lower()[-3:])
            if ((message.decode('utf-8')).lower()[-3:] == 'bye'):
                index = clients.index(client)
                clients.remove(client)
                client.close()
                alias = aliases[index]
                broadcast(f'{alias} has left the chat room!'.encode('utf-8'))
                aliases.remove(alias)
                break
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room!'.encode('utf-8'))
            aliases.remove(alias)
            break

# Main function to receive the clients connection
def receive():
    while True:
        print('Server is running and listening ...')
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024).decode('utf-8')
        aliases.append(alias)
        clients.append(client)
        print(f'The alias of this client is {alias}')
        broadcast(f'{alias} has connected to the chat room'.encode('utf-8'))
        client.send('\nyou are now connected!'.encode('utf-8'))

        # pyhton supports multi-threading
        # thread -> object
        thread = threading.Thread(target = handle_client,args = (client,))
        thread.start()

if __name__ == '__main__':
    receive()

