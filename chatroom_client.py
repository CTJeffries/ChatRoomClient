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
        self.name = tk.StringVar()
        self.name.set('')
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
        self.window.wait_window()
        return self.password.get()


class MainWindow(tk.Frame):
    '''
    DOCS
    '''
    def __init__(self, parent):
        self.parent = parent
        tk.Frame.__init__(self, parent)
        # Widgets HERE
        name = LoginWindow(self).run()
        if name != '':
            # Send name.
            pass

    def new_room():
        # Open new room window, then when its complete, open chatroom window.
        pass


    def refresh():
        # Get fresh list of rooms and update widget.
        pass


    def join_room():
        # Open pass window if there is a password, if not, open chat window.
        pass



class CreateRoomWindow():
    '''
    DOCS
    '''
    def __init__(self, parent):
        self.parent = parent
        # WIDGETS HERE

    def check_name():
        # Check if room name is ok.
        pass


class ChatRoomWindow():
    '''
    DOCS
    '''
    def __init__(self, parent):
        self.parent = parent
        # WIDGETS HERE

if __name__ == '__main__':
    root = tk.Tk()
    app = MainWindow(root)
    app.mainloop()
