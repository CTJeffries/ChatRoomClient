# Colby Jeffries & Scott Stoudt
# chatroom_server.py

'''
This script is the server for our chatroom client.

INSERT DOCS HERE

'''

# Modules
import socket
import random
import string
import threading
from cryptography.fernet import Fernet

class ChatRoom:
    '''
    This class contains an individual chat room.

    INSERT DOCS HERE

    '''
    def __init__(self, name, port, password=None, encryption=None):
        '''
        CONSTRUCTOR DOCS

        '''
        self.users = {}
        self.name = name
        self.port = port
        self.password = password
        self.encryption = encryption
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', self.port))

        self.thread = threading.Thread(target=self.run, args=())
        self.thread.start()


    def run(self):
        '''
        DOCS

        '''
        while not self.users:
            pass
        while self.users:
            data, addr = self.socket.recvfrom(1024)
            if data and (addr in self.users.keys()):
                data = data.decode()
                data = (self.users[addr] + ': ' + data + '\r\n')
                for user in self.users.keys():
                    self.socket.sendto(data.encode(), user)

        self.socket.close()



class ManagerServer:
    '''
    This class contains the overall chat server.

    INSERT DOCS HERE

    '''
    def __init__(self):
        '''
        CONSTRUCTOR DOCS

        '''
        # Initialize needed containers.
        self.chat_rooms = {}
        self.users = {}

        # Initialize entry point socket.
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverPort = 25000
        self.serverSocket.bind(('', self.serverPort))
        self.serverSocket.listen(10)

        # Infinite loop.
        while True:
            # Accept connections, save the address.
            connectionSocket, addr = self.serverSocket.accept()
            thread = threading.Thread(target=self.on_new_client, args=(connectionSocket, addr))
            thread.start()

    def on_new_client(self, connectionSocket, addr):
        while True:
            message = connectionSocket.recv(1024)
            if message:
                message_tokens = message.decode().split()
                # USER username
                # Adds uers to the global list of users.
                if message_tokens[0] == 'USER':
                    if message_tokens[1] not in self.users.keys():
                        self.users[addr] = message_tokens[1]
                        connectionSocket.send('User name added 0 \r\n'.encode())
                    else:
                        connectionSocket.send('User name in use 1 \r\n'.encode())

                # ROOM roomname *password*
                # Creates a room with the given room name and password. Password is
                # optional.
                elif message_tokens[0] == 'ROOM':
                    if message_tokens[2] not in self.chat_rooms.keys():
                        if len(message_tokens) > 3:
                            key = Fernet.generate_key()
                            pas = Fernet(key).encrypt(message_tokens[2].encode())
                        else:
                            pas = None
                            key = None

                        udp_port = message_tokens[1]
                        new_addr = (addr[0], int(udp_port))

                        port = random.randint(25001, 50000)
                        self.chat_rooms[message_tokens[2]] = ChatRoom(message_tokens[2], port, pas, key)
                        self.chat_rooms[message_tokens[2]].users[new_addr] = self.users[addr]
                        connectionSocket.send('ChatRoom established and joined {0} 0 \r\n'.format(self.chat_rooms[message_tokens[2]].port).encode())
                    else:
                        connectionSocket.send('ChatRoom name in use 1 \r\n'.encode())

                # JOIN roomname *password*
                # Joins a room with the given room name and password. Password is
                # optional.
                elif message_tokens[0] == 'JOIN':
                    if message_tokens[2] in self.chat_rooms.keys():
                        if len(message_tokens) > 3:
                            pas = message_tokens[3]
                        else:
                            pas = None

                        udp_port = message_tokens[1]
                        new_addr = (addr[0], int(udp_port))

                        if (Fernet(self.chat_rooms[message_tokens[2]].encryption).decrypt(self.chat_rooms[message_tokens[2]].password) == pas.encode()) or (pas is None and self.chat_rooms[message_tokens[2]].password is None):
                            connectionSocket.send('Connected to chat room {0} 0 \r\n'.format(self.chat_rooms[message_tokens[2]].port).encode())
                            self.chat_rooms[message_tokens[2]].users[new_addr] = self.users[addr]
                        else:
                            connectionSocket.send('Incorrect password 1 \r\n'.encode())

                else:
                    connectionSocket.send('Invalid command 1 \r\n'.encode())

            else:
                connectionSocket.send('Invalid command 1 \r\n'.encode())


if __name__ == '__main__':
    server = ManagerServer()
