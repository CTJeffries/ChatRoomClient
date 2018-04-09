# Colby Jeffries & Scott Stoudt
# chatroom_client.py

import socket
import random

sT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
p = random.randint(30000, 60000)
sT.bind(('', p))
sT.connect(('localhost', 25000))
sU = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
p2 = random.randint(30000, 60000)
sU.bind(('', p2))

def handle_room(room_port):
    while True:
        asdf = input()
        sU.sendto(asdf.encode(), ('localhost', room_port))
        data, addr = sU.recvfrom(1024)
        print(data.decode())


while True:
    x = input('Enter command: ')

    if x == 'USER':
        y = input('Enter username: ')
        sT.send(('USER ' + y).encode())
        message = sT.recv(1024).decode()
        print(message)

    elif x == 'ROOM':
        y = input('Enter room name: ')
        z = input('Enter room password: ')
        sT.send(('ROOM ' + str(p2) + ' ' + y + ' ' + z).encode())
        message = sT.recv(1024).decode()
        print(message)
        room_port = int(message.split()[-2])
        handle_room(room_port)

    elif x == 'JOIN':
        y = input('Enter room name: ')
        z = input('Enter room password: ')
        sT.send(('JOIN ' + str(p2) + ' ' + y + ' ' + z).encode())
        message = sT.recv(1024).decode()
        print(message)
        room_port = int(message.split()[-2])
        handle_room(room_port)
