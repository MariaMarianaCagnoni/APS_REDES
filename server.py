import socket         #socket for the comunication.
import threading    #alloy run multiple tasks  at the same time

HOST = '127.0.0.1'
PORT = 9090

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)        #AF_INET = IPV4   and SOCK_STREAM = TCP.
server.bind((HOST, PORT))


server.listen()
clients = []                    #empty list for clients
nicknames = []                  #empty list for nickNames

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f'{nicknames[clients.index(client)]} says {message}')
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()                                #close the connetion
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break




def receive():
    while True:
        client, address = server.accept()
        print(f"connected with{str(address)}")

        client.send("NICK".encode('UTF-8'))
        nickname = client.recv(1024)                                    #in bytes
        nicknames.append(nickname)
        clients.append(client)

        print(f'The nickname of the client is:{nickname}')
        broadcast(f"{nickname}join the chat!\n ".encode('UTF-8'))
        client.send("connect to the chat!".encode('UTF-8'))

        thread = threading.Thread(target = handle , args =(client,))
        thread.start()

print('server is running')
receive()