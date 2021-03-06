# Colby Jeffries & Scott Stoudt
# chatroom_server.py

'''
Socket Server for our AIM (Anonymous Instant Messanger) application.
'''

# Modules
import socket
import random
import string
import threading
import hashlib
import uuid
import json
import time
import queue

class ChatRoom:
    '''
    Class to hand a single chat room.
    '''
    def __init__(self, parent, name, port, password=None, salt=None):
        '''
        Initializes chat room, and starts related threads.
        '''
        self.parent = parent
        self.users = {}
        self.user_activity = {}
        self.name = name
        self.port = port
        self.max_users = 64
        self.password = password
        self.salt = salt
        self.last_listen_update = time.time()
        self.last_send_update = time.time()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', self.port))

        self.queue = queue.Queue()

        self.listener = threading.Thread(target=self.listen, args=())
        self.sender = threading.Thread(target=self.send, args=())
        self.monitor = threading.Thread(target=self.monitor_users, args=())

        self.listener.start()
        self.sender.start()
        self.monitor.start()

    def monitor_users(self):
        '''
        Monitor thread. Checks if users are active, sends alert when some one
        joins the room.
        '''
        # Initially there are no users, so we wait until there are.
        while not self.users:
            pass

        while self.users:
            if (time.time() - self.last_send_update) > 1:
                self.last_send_update = time.time()
                user_count = len(self.users)
                if len(self.users) > user_count:
                    self.queue.put('MESSAGE Someone has joined the room!'.encode())

            if (time.time() - self.last_listen_update) > 300:
                self.last_listen_update = time.time()
                users_to_boot = []
                for i in self.users.keys():
                    if (time.time() - self.user_activity[i]) > 300:
                        try:
                            self.socket.sendto('GOODBYE 0\r\n'.encode(), i)
                        except Exception as e:
                            pass
                        self.queue.put(('MESSAGE ' + self.users[i] + ' has left the room due to inactivity.\r\n').encode())
                        users_to_boot.append(i)

                for i in users_to_boot:
                    del self.users[i]
                    del self.user_activity[i]


    def listen(self):
        '''
        Listener thread. Listens for sent messages. Puts chat messages into the
        send queue, and sends goodbye message to users that quit. When this thread
        ends, the chat room destroys itself.
        '''
        # Initially there are no users, so we wait until there are.
        while not self.users:
            pass

        while self.users:
            data, addr = self.socket.recvfrom(1024)
            if data and (addr in self.users.keys()):
                self.user_activity[addr] = time.time()
                data = data.decode()
                if data.split()[0] == 'MESSAGE':
                    data = data[7:]
                    self.queue.put(('MESSAGE ' + self.users[addr] + ': ' + data + '\r\n').encode())

                elif data.split()[0] == 'QUIT':
                    try:
                        self.socket.sendto('GOODBYE 0\r\n'.encode(), addr)
                    except Exception as e:
                        pass
                    self.queue.put(('MESSAGE ' + self.users[addr] + ' has left the room.\r\n').encode())
                    del self.users[addr]
                    del self.user_activity[addr]

        self.socket.close()
        del self.parent.chat_rooms[self.name]

    def send(self):
        '''
        Sender thread. Sends any messages in the queue to all users.
        '''
        # Initially there are no users, so we wait until there are.
        while not self.users:
            pass

        user_count = len(self.users)
        while self.users:
            if not self.queue.empty():
                msg = self.queue.get()
                for user in self.users.keys():
                    try:
                        self.socket.sendto(msg, user)
                    except Exception as e:
                        pass

class ManagerServer:
    '''
    Main class for the server. Manages all connections and users.
    '''
    def __init__(self):
        '''
        Initializes the server.
        '''
        # Initialize needed containers.
        self.chat_rooms = {}
        self.users = {}

        # Guest counter.
        self.guest_counter = 1

        # Initialize entry point socket.
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverPort = 25000
        self.serverSocket.bind(('', self.serverPort))
        self.serverSocket.listen(10)

        # Infinite loop.
        while True:
            # Accept connections, and spin off thread to handle messages.
            connectionSocket, addr = self.serverSocket.accept()
            thread = threading.Thread(target=self.on_new_client, args=(connectionSocket, addr))
            thread.start()

    def on_new_client(self, connectionSocket, addr):
        '''
        Thread to handle main TCP connection.
        '''
        while True:
            message = connectionSocket.recv(1024)
            if addr not in self.users.keys():
                self.users[addr] = 'Guest {}'.format(self.guest_counter)
                self.guest_counter += 1
                if self.guest_counter > 99999:
                    self.guest_counter = 1

            if message:
                message_tokens = message.decode().split()
                # USER username
                # Adds uers to the global list of users.
                if message_tokens[0] == 'USER':
                    if message_tokens[1] not in self.users.values():
                        self.users[addr] = message_tokens[1]
                        connectionSocket.send('User name added 0\r\n'.encode())
                    else:
                        connectionSocket.send('User name in use 1\r\n'.encode())

                # ROOM roomname *password*
                # Creates a room with the given room name and password. Password is
                # optional.
                elif message_tokens[0] == 'ROOM':
                    if len(self.chat_rooms) < 30:
                        if message_tokens[2] not in self.chat_rooms.keys():
                            if len(message_tokens) > 3:
                                salt = uuid.uuid4().hex.encode()
                                pas = hashlib.sha512(message_tokens[3].encode() + salt).hexdigest()
                            else:
                                pas = None
                                salt = None

                            user_port = message_tokens[1]
                            new_addr = (addr[0], int(user_port))

                            port = random.randint(25001, 50000)
                            self.chat_rooms[message_tokens[2]] = ChatRoom(self, message_tokens[2], port, pas, salt)
                            self.chat_rooms[message_tokens[2]].users[new_addr] = self.users[addr]
                            self.chat_rooms[message_tokens[2]].user_activity[new_addr] = time.time()
                            try:
                                connectionSocket.send('ChatRoom established and joined {0} 0\r\n'.format(self.chat_rooms[message_tokens[2]].port).encode())
                            except Exception as e:
                                pass
                        else:
                            try:
                                connectionSocket.send('ChatRoom name in use 1\r\n'.encode())
                            except Exception as e:
                                pass
                    else:
                        try:
                            connectionSocket.send('All ChatRoom slots full 1\r\n'.encode())
                        except Exception as e:
                            pass

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

                        if (pas is None and self.chat_rooms[message_tokens[2]].password is None) or (hashlib.sha512(pas.encode() + self.chat_rooms[message_tokens[2]].salt).hexdigest() == self.chat_rooms[message_tokens[2]].password):
                            if len(self.chat_rooms[message_tokens[2]].users) < self.chat_rooms[message_tokens[2]].max_users:
                                try:
                                    connectionSocket.send('Connected to chat room {0} 0\r\n'.format(self.chat_rooms[message_tokens[2]].port).encode())
                                except Exception as e:
                                    pass
                                self.chat_rooms[message_tokens[2]].users[new_addr] = self.users[addr]
                                self.chat_rooms[message_tokens[2]].user_activity[new_addr] = time.time()
                        else:
                            try:
                                connectionSocket.send('Incorrect password 1\r\n'.encode())
                            except Exception as e:
                                pass
                    else:
                        try:
                            connectionSocket.send('Invlaid room 1\r\n'.encode())
                        except Exception as e:
                            pass

                # QUIT
                # Removes the user from the list.
                elif message_tokens[0] == 'QUIT':
                    del self.users[addr]
                    try:
                        connectionSocket.send('Goodbye! 0\r\n'.encode())
                    except Exception as e:
                        pass

                # INFO
                # Returns a JSON list containing information about all of the
                # rooms.
                elif message_tokens[0] == 'INFO':
                    dict_list = []
                    for i in self.chat_rooms.values():
                        temp = {}
                        temp['name'] = i.name
                        temp['users'] = len(i.users)
                        if i.password is None:
                            temp['pass'] = 0
                        else:
                            temp['pass'] = 1

                        dict_list.append(temp)

                    try:
                        connectionSocket.send(json.dumps(dict_list).encode())
                    except Exception as e:
                        pass

                else:
                    try:
                        connectionSocket.send('Invalid command 1\r\n'.encode())
                    except Exception as e:
                        pass

            else:
                try:
                    connectionSocket.send('Invalid command 1\r\n'.encode())
                except Exception as e:
                    pass


if __name__ == '__main__':
    server = ManagerServer()
