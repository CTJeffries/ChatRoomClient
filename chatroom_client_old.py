# Colby Jeffries & Scott Stoudt
# chatroom_client.py

import socket
import random
import threading

sT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
p = random.randint(30000, 60000)
sT.bind(('', p))
sT.connect(('ec2-18-216-153-185.us-east-2.compute.amazonaws.com', 25000))
sU = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
p2 = random.randint(30000, 60000)
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
            sU.sendto(('MESSAGE ' + asdf).encode(), ('ec2-18-216-153-185.us-east-2.compute.amazonaws.com', room_port))
        else:
            sU.sendto('QUIT'.encode(), ('ec2-18-216-153-185.us-east-2.compute.amazonaws.com', room_port))

def recieve_room(room_port):
    while True:
        data, addr = sU.recvfrom(1024)
        print(data.decode())


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
