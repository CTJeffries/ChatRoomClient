# Colby Jeffries and Scott Stoudt
# serve_chatclient.py

import os
import subprocess
from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/chatclient/source')
def send_client_source():
    return send_from_directory(os.getcwd(), 'chatroom_client.py')

if __name__ == '__main__':
    subprocess.call(['./get_serversh'])
    app.run(host='0.0.0.0', port=24999, threaded=True)
