# Colby Jeffries & Scott Stoudt
# chatroom_client.py

import socket
import random
import threading
import tkinter as tk
from tkinter import messagebox
import json
import sys
import queue
import time
import os


class IPWindow(object):
    '''
    DOCS
    '''
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.configure(background='grey')
        self.window.resizable(height = False, width = False)
        self.window.title('AIM (Anonymous Instant Messenger)')
        self.window.attributes("-topmost", True)
        self.window.bind('<Return>', lambda x: self.window.destroy())
        self.window.grab_set()
        self.window.protocol("WM_DELETE_WINDOW", self.onDestroy)
        self.ip = tk.StringVar()
        self.ip.set('')

        self.cancelled = False

        RWidth = root.winfo_screenwidth()
        RHeight = root.winfo_screenheight()
        WindowWidth = 200
        WindowHeight = 100
        self.window.geometry(("%dx%d+%d+%d")%(WindowWidth,WindowHeight,(RWidth/2)-(WindowWidth/2),(RHeight/2)-(WindowHeight/2)))

        self.label = tk.Label(self.window, text='Enter server IP', highlightbackground='grey', background='grey')
        self.label.pack()

        self.server_ip = tk.Entry(self.window, textvariable=self.ip, validate='all', validatecommand=(self.window.register(self.validate), '%P'), highlightbackground='grey')
        self.server_ip.pack()

        self.enter_button = tk.Button(self.window, text='Enter', command=self.window.destroy, highlightbackground='grey', background='#9955DD')
        self.enter_button.pack()
        self.window.lift()
        self.window.update()
        self.parent.parent.update()

    def onDestroy(self):
        self.cancelled = True
        self.window.destroy()

    def run(self):
        self.window.wait_window()
        self.window.grab_release()
        if self.cancelled or self.ip.get() == '':
            sys.exit(-1)
        else:
            return self.ip.get()

    def validate(self, P):
        if (len(P) <= 50) or P == '':
            return True
        else:
            return False


class LoginWindow(object):
    '''
    DOCS
    '''
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.configure(background='grey')
        self.window.bind('<Return>', lambda x: self.submit())
        self.window.resizable(height = False, width = False)
        self.window.attributes("-topmost", True)
        self.window.grab_set()
        self.window.title('AIM (Anonymous Instant Messenger)')
        self.window.protocol("WM_DELETE_WINDOW", self.onDestroy)

        RWidth = root.winfo_screenwidth()
        RHeight = root.winfo_screenheight()
        WindowWidth = 350
        WindowHeight = 120
        self.window.geometry(("%dx%d+%d+%d")%(WindowWidth,WindowHeight,(RWidth/2)-(WindowWidth/2),(RHeight/2)-(WindowHeight/2)))

        self.greeting = tk.Label(self.window, text= 'Hello! Welcome to AIM:\n Anonymous Instant Messenger', highlightbackground='grey', background='grey')
        self.greeting.pack()

        self.name = tk.StringVar()
        self.name.set('')
        self.label = tk.Label(self.window, text='Enter a username or leave blank to enter as a guest!', highlightbackground='grey', background='grey')
        self.label.pack()
        self.entry = tk.Entry(self.window, textvariable=self.name, validate='all', validatecommand=(self.window.register(self.validate), '%P'), highlightbackground='grey')
        self.entry.pack()
        self.enter = tk.Button(self.window, text='Ok', command=self.submit, highlightbackground='grey', background='#9955DD')
        self.enter.pack()
        self.window.lift()
        self.window.update()
        self.parent.parent.update()

    def onDestroy(self):
        self.name.set('')
        self.window.destroy()

    def validate(self, P):
        if ((len(P) <= 20) and P.isalnum()) or P == '':
            return True
        else:
            return False

    def submit(self):
        self.window.destroy()

    def run(self):
        self.window.wait_window()
        self.window.grab_release()
        return self.name.get()


class PassWindow():
    '''
    DOCS
    '''
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.configure(background='grey')
        self.window.bind('<Return>', lambda x: self.window.destroy)
        self.window.resizable(height = False, width = False)
        self.window.title('AIM (Anonymous Instant Messenger)')
        self.window.attributes("-topmost", True)
        self.window.grab_set()
        self.window.protocol("WM_DELETE_WINDOW", self.onDestroy)
        self.password = tk.StringVar()
        self.password.set('')

        self.cancelled = False

        RWidth = root.winfo_screenwidth()
        RHeight = root.winfo_screenheight()
        WindowWidth = 200
        WindowHeight = 100
        self.window.geometry(("%dx%d+%d+%d")%(WindowWidth,WindowHeight,(RWidth/2)-(WindowWidth/2),(RHeight/2)-(WindowHeight/2)))

        self.label = tk.Label(self.window, text='Enter room password', highlightbackground='grey', background='grey')
        self.label.pack()

        self.room_pass = tk.Entry(self.window, textvariable=self.password, validate='all', validatecommand=(self.window.register(self.validate), '%P'), highlightbackground='grey')
        self.room_pass.pack()

        self.enter_button = tk.Button(self.window, text='Join Room', command=self.window.destroy, highlightbackground='grey', background='#9955DD')
        self.enter_button.pack()
        self.window.lift()
        self.window.update()
        self.parent.parent.update()

    def onDestroy(self):
        self.cancelled = True
        self.window.destroy()

    def run(self):
        self.window.wait_window()
        self.window.grab_release()
        if self.cancelled or self.password.get() == '':
            return None
        else:
            return self.password.get()

    def validate(self, P):
        if ((len(P) <= 20) and P.isalnum()) or P == '':
            return True
        else:
            return False


class MainWindow(tk.Frame):
    '''
    DOCS
    '''
    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(background='grey')
        self.parent.resizable(height = False, width = False)
        self.parent.title('AIM (Anonymous Instant Messenger)')
        tk.Frame.__init__(self, parent)
        self.parent.protocol("WM_DELETE_WINDOW", self.onDestroy)

        RWidth = root.winfo_screenwidth()
        RHeight = root.winfo_screenheight()
        WindowWidth = 400
        WindowHeight = 800
        self.parent.geometry(("%dx%d+%d+%d")%(WindowWidth, WindowHeight, (RWidth/2)-(WindowWidth/2), (RHeight/2)-(WindowHeight/2)))

        self.udp_sockets = []
        self.udp_usage = []

        self.name_button = tk.Button(self.parent, text = "Back to Login", command=self.handle_login, highlightbackground='grey', background='#9955DD')
        self.refresh_button = tk.Button(self.parent, text = "Refresh Rooms", command=self.refresh, highlightbackground='grey', background='#9955DD')
        self.join_button = tk.Button(self.parent, text = "Join", command=self.join_room, state='disabled', highlightbackground='grey', background='#9955DD')
        self.create_button = tk.Button(self.parent, text = "Create Room", command=self.new_room, highlightbackground='grey', background='#9955DD')

        self.name_button.grid(row=0, column=0, sticky='nsew')
        self.refresh_button.grid(row=0, column=1, sticky='nsew')
        self.join_button.grid(row=0, column=2, sticky='nsew')
        self.create_button.grid(row=0, column=3, sticky='nsew')

        self.name_label = tk.Label(self.parent, text='Room Name', highlightbackground='grey', background='grey')
        self.status_label = tk.Label(self.parent, text='Status', highlightbackground='grey', background='grey')
        self.pop_label = tk.Label(self.parent, text='Users', highlightbackground='grey', background='grey')

        self.name_label.grid(row=1, column=0, columnspan=2, sticky='nsew')
        self.status_label.grid(row=1, column=2, sticky='nsew')
        self.pop_label.grid(row=1, column=3, sticky='nsew')

        self.server = ''

        if os.path.isfile('server.txt'):
            with open('server.txt', 'r') as f:
                self.server = f.readline()

            if self.server[-1] == '\n':
                self.server = self.server[0:-1]

        else:
            self.server = IPWindow(self).run()

        try:
            self.used_ports = []
            self.main_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_port = random.randint(30000, 50000)
            self.used_ports.append(self.tcp_port)
            self.main_tcp.bind(('', self.tcp_port))
            self.main_tcp.connect((self.server, 25000))
        except Exception as e:
            print(e)
            sys.exit(-1)

        self.selected_room = tk.IntVar()
        self.selected_room.set(0)
        self.room_buttons = []
        self.rooms = []
        self.chat_rooms = []
        self.refresh()
        self.parent.update()

        self.handle_login()
        self.parent.after(30000, self.auto_refresh)

    def onDestroy(self):
        if not self.chat_rooms:
            self.main_tcp.send('QUIT'.encode())
            self.main_tcp.close()
            for i in self.udp_sockets:
                i[0].close()

            self.parent.destroy()

    def handle_login(self):
        # Open the name window. Repeats until a unused name is found.
        ok = 1
        name = LoginWindow(self).run()
        while ok == 1:
            if name != '':
                try:
                    self.main_tcp.send(('USER ' + name).encode())
                    message = self.main_tcp.recv(1024).decode()
                    ok = message.split()[-1]
                except Exception as e:
                    print(e)
                if ok == 1:
                    messagebox.showinfo('Alert!', message[:-3], parent=self.parent)
                    name = LoginWindow(self).run()
            else:
                ok = 0

    def new_room(self):
        # Open new room window, then when its complete, open chatroom window.
        room = CreateRoomWindow(self).run()
        if room is not None:
            sock = self.get_sock()
            try:
                self.main_tcp.send(('ROOM ' + str(sock[1][1]) + ' ' + room[0] + ' ' + room[1]).encode())
                message = self.main_tcp.recv(1024).decode()
                if message.split()[-1] == '0':
                    room_port = int(message.split()[-2])
                    self.chat_rooms.append(ChatRoomWindow(self, room_port, sock, len(self.chat_rooms)))
                else:
                    messagebox.showinfo('Alert!', message[:-3], parent=self.parent)
            except Exception as e:
                print(e)

    def refresh(self):
        for i in self.room_buttons:
            for j in i:
                j.grid_forget()

        self.room_buttons = []
        self.rooms = []

        try:
            self.main_tcp.send('INFO'.encode())
            self.rooms = json.loads(self.main_tcp.recv(1024).decode())

            for i in range(len(self.rooms)):
                room = self.rooms[i]['name']
                if self.rooms[i]['pass'] == 0:
                    pass_status = ' OPEN '
                else:
                    pass_status = 'CLOSED'

                count = str(self.rooms[i]['users']) + '/64'

                self.room_buttons.append([tk.Radiobutton(self.parent, text=room, variable=self.selected_room, value=i, indicatoron=False, highlightbackground='grey', background='#9955DD'), tk.Label(self.parent, text=pass_status, highlightbackground='grey', background='grey'), tk.Label(self.parent, text=count, highlightbackground='grey', background='grey')])
                self.room_buttons[i][0].grid(row=i+2, column=0, columnspan=2, sticky='nsew')
                self.room_buttons[i][1].grid(row=i+2, column=2, sticky='nsew')
                self.room_buttons[i][2].grid(row=i+2, column=3, sticky='nsew')

            if len(self.rooms) > 0:
                self.join_button.config(state='normal')
            else:
                self.join_button.config(state='disabled')

        except Exception as e:
            print(e)

    def join_room(self):
        # Open pass window if there is a password, if not, open chat window.
        sock = self.get_sock()
        if self.rooms[self.selected_room.get()]['pass']:
            passwrd = PassWindow(self).run()
        else:
            passwrd = ''

        if passwrd is not None:
            try:
                self.main_tcp.send(('JOIN ' + str(sock[1][1]) + ' ' + self.rooms[self.selected_room.get()]['name'] + ' ' + passwrd).encode())
                message = self.main_tcp.recv(1024).decode()
                if message.split()[-1] == '0':
                    room_port = int(message.split()[-2])
                    self.chat_rooms.append(ChatRoomWindow(self, room_port, sock, len(self.chat_rooms)))
                else:
                    messagebox.showinfo('Alert!', message[:-3], parent=self.parent)
            except Exception as e:
                print(e)

    def generate_udp_port(self):
        new_port = random.randint(30000, 50000)
        while new_port in self.used_ports:
            new_port = random.randint(30000, 50000)

        self.used_ports.append(new_port)
        self.udp_usage.append(False)
        self.udp_sockets.append((socket.socket(socket.AF_INET, socket.SOCK_DGRAM), new_port))
        self.udp_sockets[-1][0].bind(('', new_port))

    def get_sock(self):
        for i in range(len(self.udp_sockets)):
            if self.udp_usage[i] == False:
                self.udp_usage[i] = True
                return (i, self.udp_sockets[i])

        self.generate_udp_port()
        self.udp_usage[-1] = True
        return (len(self.udp_sockets) - 1, self.udp_sockets[-1])

    def auto_refresh(self):
        self.refresh()
        self.parent.after(30000, self.auto_refresh)


class CreateRoomWindow():
    '''
    DOCS
    '''
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.configure(background='grey')
        self.window.bind('<Return>', lambda x: self.submit())
        self.window.resizable(height = False, width = False)
        self.window.title('AIM (Anonymous Instant Messenger)')
        self.window.attributes("-topmost", True)
        self.window.grab_set()
        self.window.protocol("WM_DELETE_WINDOW", self.cancel)
        self.room_name = tk.StringVar()
        self.room_name.set('')
        self.room_pass = tk.StringVar()
        self.room_pass.set('')
        self.cancelled = False

        self.name_label = tk.Label(self.window, text='Give your room a name', highlightbackground='grey', background='grey')
        self.name_label.grid(row=0, column=0, columnspan=2, sticky='nsew')

        self.new_room_name = tk.Entry(self.window, textvariable=self.room_name, validate='all', validatecommand=(self.window.register(self.validate), '%P'), highlightbackground='grey')
        self.new_room_name.grid(row=1, column=0, columnspan=2, sticky='nsew')

        self.pass_label = tk.Label(self.window, text='Enter a password for your room. Leave blank for an open room', highlightbackground='grey', background='grey')
        self.pass_label.grid(row=2, column=0, columnspan=2, sticky='nsew')

        self.new_room_pass = tk.Entry(self.window, textvariable=self.room_pass, validate='all', validatecommand=(self.window.register(self.validate), '%P'), highlightbackground='grey')
        self.new_room_pass.grid(row=3, column=0, columnspan=2, sticky='nsew')

        self.create_button = tk.Button(self.window, text='Create Room', command=self.submit, highlightbackground='grey', background='#9955DD')
        self.create_button.grid(row=4, column=0, sticky='nsew')

        self.return_button = tk.Button(self.window, text='Cancel', command=self.cancel, highlightbackground='grey', background='#9955DD')
        self.return_button.grid(row=4, column=1, sticky='nsew')
        self.window.lift()
        self.window.update()
        self.parent.parent.update()

    def submit(self):
        self.window.destroy()

    def run(self):
        self.window.wait_window()
        self.window.grab_release()
        if self.room_name.get() == '' or self.cancelled:
            return None
        else:
            return (self.room_name.get(), self.room_pass.get())

    def cancel(self):
        self.cancelled = True
        self.window.destroy()

    def validate(self, P):
        if ((len(P) <= 20) and P.isalnum()) or P == '':
            return True
        else:
            return False


class ChatRoomWindow():
    '''
    DOCS
    '''
    def __init__(self, parent, port, sock, index):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.configure(background='grey')
        self.window.bind('<Return>', lambda x: self.send_message()
        )
        self.window.resizable(height = False, width = False)
        self.window.title('AIM (Anonymous Instant Messenger)')
        self.window.protocol("WM_DELETE_WINDOW", self.onDestroy)
        self.port = port
        self.sock = sock
        self.index = index
        self.open = True
        self.queue = queue.Queue()
        self.message = tk.StringVar()
        self.message.set('')
        self.chat_box = tk.Text(self.window, state='disabled', highlightbackground='grey')
        self.chat_box.grid(row=0, column=0, columnspan=3, sticky='nsew')

        self.input = tk.Entry(self.window, textvariable=self.message, highlightbackground='grey')
        self.input.grid(row=1, column=0, columnspan=2, sticky='nsew')

        self.enter_button = tk.Button(self.window, text='Enter', command=self.send_message, highlightbackground='grey', background='#9955DD')
        self.enter_button.grid(row= 1, column=2, sticky='nsew')

        self.rcv_thread = threading.Thread(target=self.recieve)
        self.rcv_thread.start()
        self.parent.parent.after(100, self.check)
        self.window.update()
        self.parent.parent.update()

    def onDestroy(self):
        self.sock[1][0].sendto('QUIT'.encode(), (self.parent.server, self.port))
        self.parent.udp_usage[self.sock[0]] = False
        self.open = False
        del self.parent.chat_rooms[self.index]
        self.window.destroy()

    def recieve(self):
        while True:
            data, addr = self.sock[1][0].recvfrom(1024)
            data = data.decode()
            if data.split()[0] == 'MESSAGE':
                self.queue.put(data[7:-2])
            elif data.split()[0] == 'GOODBYE':
                if self.open:
                    self.onDestroy()

                break

    def send_message(self):
        self.sock[1][0].sendto(('MESSAGE ' + self.message.get()).encode(), (self.parent.server, self.port))
        self.message.set('')

    def check(self):
        if not self.queue.empty():
            self.chat_box.config(state='normal')
            self.chat_box.insert('end', self.queue.get() + '\n')
            self.chat_box.config(state='disabled')
            self.chat_box.see('end')

        if self.open:
            self.parent.parent.after(100, self.check)


if __name__ == '__main__':
    root = tk.Tk()
    app = MainWindow(root)
    app.mainloop()
