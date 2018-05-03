# Colby Jeffries and Scott Stoudt
# serve_chatclient.py

'''
Flask application to serve the source code and compiled clients. Meant to be
hosted on AWS.
'''

# Modules
import os
import subprocess
from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/chatclient/source')
def send_client_source():
    '''
    Return source code.
    '''
    return send_from_directory(os.getcwd(), 'chatroom_client.py')

@app.route('/chatclient/windows')
def send_client_windows():
    '''
    Return zipped windows executable.
    '''
    return send_from_directory(os.getcwd(), os.path.join('dist', 'chatroom_client_windows.zip'))

@app.route('/chatclient/linux')
def send_client_linux():
    '''
    Return zipped linux executable.
    '''
    return send_from_directory(os.getcwd(), os.path.join('dist', 'chatroom_client_linux.zip'))

@app.route('/chatclient/mac')
def send_client_mac():
    '''
    Return zipped MacOS executable.
    '''
    return send_from_directory(os.getcwd(), os.path.join('dist', 'chatroom_client_mac.zip'))

if __name__ == '__main__':
    # Call shell script to update the server.txt file with the current server.
    # Not really useful anymore.
    subprocess.call(['./get_server.sh'])
    # Start up the server, open to the internet.
    app.run(host='0.0.0.0', port=24999, threaded=True)
