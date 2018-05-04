# ChatRoomClient

## To Run
The server can be run with:

`python3 chatroom_server.py`

Similarly, the client can be run with:

`python3 chatroom_client.py`

A quick note about the client. The client reads the server.txt file for the
server IP if the file is present. This is so the the IP does not need typed
repeatedly. However, if the server changes IP, the text file needs changed or
removed.

## Requirements
The following python packages are required:
- socket
- random
- string
- threading
- hashlib
- uuid
- json
- time
- queue
- tkinter
- sys
- os

All but one of these are included in the default python install. To get the single non-default package, run:

`pip3 install -r requirements.txt`

This installs uuid. If you do not have Tkinter, find a tutorial for your operating system and follow that. Tkinter can be a pain to install if you did not get it by default with Python (most python distributions include it).

## Recommended Deployment
The way we hosted our server was with an EC2 instance on AWS.
We recommend hosting both the server and flask app on the AWS server so that
it can be accessed around the world, and users do not need python to run it.
The flask app can be run with:

`python3 server_chatclient.py.`

Flask apps are not really great for high traffic situations, but we believe that
our chat application would be overwhelmed well before the Flask app would be.
