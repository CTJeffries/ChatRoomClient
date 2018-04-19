# Colby Jeffries and Scott Stoudt
# serve_chatclient.py

import os
from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/chatclient')
def send_client():
    return send_from_directory(os.getcwd(), 'chatroom_client.py')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=24999, threaded=True)
