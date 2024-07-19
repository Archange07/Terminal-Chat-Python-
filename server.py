import threading
import socket

ipv4 = '127.0.0.1'
port = 5050

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ipv4, port))
server.listen()

users = []
user_names = []


def broadcast(message):
    for user in users:
        user.send(message)


def handle(client):

    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = users.index(client)
            users.remove(client)
            client.close()
            user_name = user_names[index]


            broadcast(f'[-] {user_name} has left the chat'.encode('utf-8'))
            user_names.remove(user_name)
            break


def receive():
    while True:
        client, address = server.accept()
        print(f'[+] Successfully connected to {str(address)}...')

        client.send('NICK'.encode('utf-8'))
        user_name = client.recv(1024).decode('utf-8')
        user_names.append(user_name)
        users.append(client)

        print(f'[+] {user_name} has joined the server')
        broadcast(f'[+] {user_name} joined the chat...\n'.encode('utf-8'))

        client.send("[+] Connected to the server...".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        print(f'Threads: {threading.active_count()}')


print(f'Server is active on port {port} and address {ipv4}')

receive()
