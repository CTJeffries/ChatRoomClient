# Colby Jeffries & Scott Stoudt
# chatroom_client.py

import socket
import random
import threading
import tkinter as tk
import json

class LoginWindow(object):
    '''
    DOCS
    '''
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)

        RWidth = root.winfo_screenwidth()
        RHeight = root.winfo_screenheight()
        WindowWidth = 400
        WindowHeight = 200
        self.window.geometry(("%dx%d+%d+%d")%(WindowWidth,WindowHeight,(RWidth/2)-(WindowWidth/2),(RHeight/2)-(WindowHeight)))

        self.name = tk.StringVar()
        self.name.set('')
        self.label = tk.Label(self.window, text='Enter a username or leave blank to enter as a guest!')
        self.label.pack()
        self.entry = tk.Entry(self.window, textvariable=self.name, validate='all',
                                validatecommand=(self.window.register(self.validate), '%P'))
        self.entry.pack()
        self.enter = tk.Button(self.window, text='Ok', command=self.submit)
        self.enter.pack()

    def validate(self, P):
        if len(P) <= 20:
            return P.isalnum()
        else:
            return False

    def submit(self):
        self.window.destroy()

    def run(self):
        self.window.wait_window()
        return self.name.get()


class PassWindow():
    '''
    DOCS
    '''
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.password = tk.StringVar()
        self.password.set('')

        self.label = tk.Label(self.window, text='Enter room password')
        self.label.pack()

        self.room_pass = tk.Entry(self.window, textvariable=self.password, validate='all',
                                validatecommand=(self.window.register(self.validate), '%P'))
        self.room_pass.pack()

        self.enter_button = tk.Button(self.window, text='Join Room', command=self.join_room)
        self.enter_button.pack()

    def run(self):
        self.window.wait_window()
        return self.password.get()

    def validate(self, P):
        if len(P) <= 20:
            return P.isalnum()
        else:
            return False

    def run(self):
        self.window.wait_window()
        return self.name.get()


class MainWindow(tk.Frame):
    '''
    DOCS
    '''
    def __init__(self, parent):
        self.parent = parent
        tk.Frame.__init__(self, parent)

        self.used_ports = []
        self.main_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_port = random.randint(30000, 50000)
        self.used_ports.append(self.tcp_port)
        self.main_tcp.bind(('', self.tcp_port))
        self.main_tcp.connect(('ec2-18-217-72-186.us-east-2.compute.amazonaws.com', 25000))

        self.udp_sockets = []
        self.udp_usage = []

        RWidth = root.winfo_screenwidth()
        RHeight = root.winfo_screenheight()
        WindowWidth = 600
        self.parent.geometry(("%dx%d+%d+%d")%(WindowWidth,RHeight,(RWidth/2)-(WindowWidth/2),0))

        self.name_button = tk.Button(self.parent, text = "Back to Login")
        self.name_button.grid(row=1, column=0, sticky='NSEW')

        self.refresh_button = tk.Button(self.parent, text = "Refresh Rooms", command=self.refresh)
        self.refresh_button.grid(row=1, column=1, sticky='NSEW')

        self.name_button = tk.Button(self.parent, text = "Back to Login", command=self.handle_login)
        self.refresh_button = tk.Button(self.parent, text = "Refresh Rooms", command=self.refresh)
        self.join_button = tk.Button(self.parent, text = "Join", command=self.join_room)
        self.create_button = tk.Button(self.parent, text = "Create Room", command=self.new_room)

        self.selected_room = tk.IntVar()
        self.selected_room.set(0)
        self.room_buttons = []
        self.rooms = []
        self.refresh()

        self.handle_login()

    def handle_login(self):
        # Open the name window. Repeats until a unused name is found.
        ok = 1
        name = LoginWindow(self).run()
        while ok == 1:
            if name != '':
                self.main_tcp.send(('USER ' + name).encode())
                message = self.main_tcp.recv(1024).decode()
                ok = message.split()[-1]
                if ok == 1:
                    tk.messagebox.showinfo('Alert!', message[:-3])
                    name = LoginWindow(self).run(

            else:
                ok = 0

    def new_room(self):
        # Open new room window, then when its complete, open chatroom window.
        room = CreateRoomWindow(self).run()
        if room is not None:
            sock = self.get_socket()
            self.main_tcp.send(('ROOM ' + str(sock[1][1]), + ' ' + room[0] + ' ' + room[1]))
            self.udp_index += 1
            message = self.main_tcp.recv(1024).decode()
            if message.split()[-1] == '0':
                room_port = int(message.split()[-2])
                ChatRoomWindow(self, room_port, sock).run()
            else:
                tk.messagebox.showinfo('Alert!', message[:-3])


    def refresh(self):
        self.room_buttons = []
        self.rooms = []

        self.main_tcp.send('INFO'.encode())
        self.rooms = json.loads(self.main_tcp.recv(1024).decode())

        for i in range(len(self.rooms)):
            if self.rooms[i]['pass'] == 0:
                room = self.rooms[i]['name'] + '    OPEN    ' + str(self.rooms[i]['users']) + '/64'
            else:
                room = self.rooms[i]['name'] + '   ClOSED   ' + str(self.rooms[i]['users']) + '/64'

            self.room_buttons.append(tk.Radiobutton(self.parent, text=room, variable=self.selected_room, value=i))
            self.room_buttons[i].grid(row=i, column=0, columnspan=4)

        self.name_button.grid_forget()
        self.refresh_button.grid_forget()
        self.join_button.grid_forget()
        self.create_button.grid_forget()

        self.name_button.grid(row=len(self.rooms), column=0)
        self.refresh_button.grid(row=len(self.rooms), column=1)
        self.join_button.grid(row=len(self.rooms), column=2)
        self.create_button.grid(row=len(self.rooms), column=3)

    def join_room(self):
        # Open pass window if there is a password, if not, open chat window.
        passwrd = PassWindow(self).run()


    def generate_udp_port(self):
        new_port = random.randint(30000, 50000)
        while new_port in self.used_ports:
            new_port = random.randint(30000, 50000)

        self.udp_usage.append(False)
        self.udp_sockets.append((socket.socket(socket.AF_INET, socket.SOCK_DGRAM), new_port))
        self.udp_sockets[-1][0].bind(('', new_port))

    def get_sock(self):
        for i in range(len(self.udp_port)):
            if self.udp_usage[i] == False:
                self.udp_usage[i] = True
                return (i, self.udp_sockets[i])

        generate_udp_port()
        self.udp_usage[-1] = True
        return (len(self.udp_sockets) - 1, self.udp_sockets[-1])



class CreateRoomWindow():
    '''
    DOCS
    '''
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.room_name = tk.StringVar()
        self.room_name.set('')
        self.room_pass = tk.StringVar()
        self.room_pass.set('')
        self.canceled = False

        self.name_label = tk.Label(self.window, text='Give your room a name')
        self.name_label.grid(row=0, column=1)

        self.new_room_name = tk.Entry(self.window, textvariable=self.room_name, validate='all',
                                validatecommand=(self.window.register(self.validate), '%P'))
        self.new_room_name.grid(row=1, column=1)

        self.pass_label = tk.Label(self.window, text='Enter a password for your room. Leave blank for an open room')
        self.pass_label.grid(row=2, column=1)

        self.new_room_pass = tk.Entry(self.window, textvariable=self.room_pass, validate='all',
                                validatecommand=(self.window.register(self.validate), '%P'))
        self.new_room_pass.grid(row=3, column=1)

        self.create_button = tk.Button(self.window, text='Create Room', command=self.submit)
        self.create_button.grid(row=4, column=0)

        self.return_button = tk.Button(self.window, text='Cancel', command=self.cancel)
        self.return_button.grid(row=4, column=2)

    def submit(self):
        self.window.destory()

    def run(self):
        self.window.wait_window()
        if self.room_name == '' or self.canceled:
            return None
        else:
            return (self.room_name.get(), self.room_pass.get())

    def cancel(self):
        self.canceled = True

    def validate(self, P):
        if len(P) <= 20:
            return P.isalnum()
        else:
            return False


class ChatRoomWindow():
    '''
    DOCS
    '''
    def __init__(self, parent, port, sock):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        # WIDGETS HERE
        self.input = tk.Entry(self.window)
        self.input.grid(row=1, column=0, columnspan=3)

        self.enter_button = tk.Button(self.window, text='Enter', command=self.send_message)
        self.enter_button.grid(row= 1, column=3)

    def send_message(self):
        pass


if __name__ == '__main__':
    root = tk.Tk()
    app = MainWindow(root)
    app.mainloop()
