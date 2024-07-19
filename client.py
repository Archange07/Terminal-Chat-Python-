import sys
import threading
import socket
import time

user_name = input("Please enter your name: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5050))


def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(user_name.encode('utf-8'))
            else:
                print(message)
                sys.stdout.flush()
        except:
            print("[-] Connection Failed!")
            client.close()
            break


def write():
    while True:
        user_input = input("")
        if user_input.strip():
            message = f'{time.strftime("[%I:%M %p]")} {user_name}: {user_input}'
            client.send(message.encode('utf-8'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
