# Colby Jeffries & Scott Stoudt
# chatroom_client.py

import socket
import random
import threading
import tkinter as tk


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
        self.entry = tk.Entry(self.window, textvariable=self.name)
        self.entry.pack()
        self.enter = tk.Button(self.window, text='Ok', command=self.check_name)
        self.enter.pack()


    def check_name(self):
        if (len(self.name.get()) >= 3 or len(self.name.get()) <= 20) or (self.name.get() == ''):
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
        # Widgets HERE
        self.label = tk.Label(self.window, text='Enter room password')
        self.label.pack()

        self.room_pass = tk.Entry(self.window)
        self.room_pass.pack()

        self.enter_button = tk.Button(self.window, text='Join Room', command=self.join_room)
        self.enter_button.pack()

        self.window.wait_window()
        return self.password.get()

    def join_room(self):
        #ChatRoomWindow(self).run()
        pass

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

        RWidth = root.winfo_screenwidth()
        RHeight = root.winfo_screenheight()
        WindowWidth = 600
        self.parent.geometry(("%dx%d+%d+%d")%(WindowWidth,RHeight,(RWidth/2)-(WindowWidth/2),0))
        # Widgets HERE
        ## Radio buttons

        self.name_button = tk.Button(self.parent, text = "Back to Login")
        self.name_button.grid(row=1, column=0, sticky='NSEW')

        self.refresh_button = tk.Button(self.parent, text = "Refresh Rooms", command=self.refresh)
        self.refresh_button.grid(row=1, column=1, sticky='NSEW')

        self.join_button = tk.Button(self.parent, text = "Join", command=self.join_room)
        self.join_button.grid(row=1, column=2, sticky='NSEW')

        self.create_button = tk.Button(self.parent, text = "Create Room", command=self.new_room)
        self.create_button.grid(row=1, column=3, sticky='NSEW')

        name = LoginWindow(self).run()
        if name != '':
            # Send name.
            pass

    def new_room(self):
        # Open new room window, then when its complete, open chatroom window.
        CreateRoomWindow(self).run()
        pass


    def refresh(self):
        # Get fresh list of rooms and update widget.
        pass


    def join_room(self):
        # Open pass window if there is a password, if not, open chat window.
        PassWindow(self).run()
        pass



class CreateRoomWindow():
    '''
    DOCS
    '''
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        # WIDGETS HERE
        self.name_label = tk.Label(self.window, text='Give your room a name')
        self.name_label.grid(row=0, column=1)

        self.new_room_name = tk.Entry(self.window)
        self.new_room_name.grid(row=1, column=1)

        self.pass_label = tk.Label(self.window, text='Enter a password for your room. Leave blank for an open room')
        self.pass_label.grid(row=2, column=1)

        self.new_room_pass = tk.Entry(self.window)
        self.new_room_pass.grid(row=3, column=1)

        self.create_button = tk.Button(self.window, text='Create Room', command=self.check_name)
        self.create_button.grid(row=4, column=0)

        self.return_button = tk.Button(self.window, text='Cancel', command=self.window.destroy)
        self.return_button.grid(row=4, column=2)

    def check_name(self):
        # Check if room name is ok.
        pass

    def run(self):
        self.window.wait_window()
        return self.name.get()


class ChatRoomWindow():
    '''
    DOCS
    '''
    def __init__(self, parent):
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
