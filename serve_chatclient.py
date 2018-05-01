# Colby Jeffries and Scott Stoudt
# serve_chatclient.py

import os
import subprocess
from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/chatclient/source')
def send_client_source():
    return send_from_directory(os.getcwd(), 'chatroom_client.py')

@app.route('/chatclient/windows')
def send_client_windows():
    return send_from_directory(os.getcwd(), os.path.join('dist', 'chatroom_client_windows.exe'))

@app.route('/chatclient/linux')
def send_client_linux():
    return send_from_directory(os.getcwd(), os.path.join('dist', 'chatroom_client_linux'))

@app.route('/chatclient/mac')
def send_client_mac():
    return send_from_directory(os.getcwd(), os.path.join('dist', 'chatroom_client_mac'))

if __name__ == '__main__':
    subprocess.call(['./get_server.sh'])
    app.run(host='0.0.0.0', port=24999, threaded=True)
