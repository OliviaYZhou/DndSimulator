from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
socketIo = SocketIO(app, cors_allowed_origins="*")

from dice_server import *

from character_server import *

if __name__ == '__main__':

    # app.run(debug=True)
    socketIo.run(app)