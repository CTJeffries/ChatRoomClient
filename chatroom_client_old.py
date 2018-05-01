# Colby Jeffries & Scott Stoudt
# chatroom_client.py

import socket
import random
import threading

with open('server.txt', 'r') as f:
    server = f.readline()
if server[-1] == '\n':
    server = server[0:-1]

sT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
p = random.randint(30000, 50000)
sT.bind(('', p))
sT.connect((server, 25000))
sU = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
p2 = random.randint(30000, 50000)
sU.bind(('', p2))


def handle_room(room_port):
    rcv_thread = threading.Thread(target=recieve_room, args=(room_port,))
    rcv_thread.start()
    send_thread = threading.Thread(target=send_room, args=(room_port,))
    send_thread.start()
    rcv_thread.join()
    send_thread.join()


def send_room(room_port):
    while True:
        asdf = input()
        if asdf.lower() != 'quit':
            sU.sendto(('MESSAGE ' + asdf).encode(), (server, room_port))
        else:
            sU.sendto('QUIT'.encode(), (server, room_port))
            break

def recieve_room(room_port):
    while True:
        data, addr = sU.recvfrom(1024)
        data = data.decode()
        if data.split()[0] == 'MESSAGE':
            print(data[7:])
        elif data.split()[0] == 'GOODBYE':
            break



def basic_client():
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
            if message.split()[-1] == '0':
                room_port = int(message.split()[-2])
                handle_room(room_port)

        elif x == 'JOIN':
            y = input('Enter room name: ')
            z = input('Enter room password: ')
            sT.send(('JOIN ' + str(p2) + ' ' + y + ' ' + z).encode())
            message = sT.recv(1024).decode()
            print(message)
            if message.split()[-1] == '0':
                room_port = int(message.split()[-2])
                handle_room(room_port)

        elif x == 'INFO':
            sT.send('INFO'.encode())
            message = sT.recv(1024).decode()
            print(message)

        elif x== 'QUIT':
            sT.send('QUIT'.encode())
            message = sT.recv(1024).decode()
            print(message)
            break


if __name__ == '__main__':
    basic_client()
