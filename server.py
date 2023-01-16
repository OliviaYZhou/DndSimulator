from flask import Flask, render_template, session, request
# from flask_restful import Api
from flask_socketio import SocketIO, emit
import psycopg2


app = Flask(__name__)
api = Api(app)
socketIo = SocketIO(app, cors_allowed_origins="*")
from backend.dice_server import *
from backend.character_server import *

conn = psycopg2.connect("dbname=dndtoolkitdb user=olivia")
# cur = conn.cursor()

app.route('/')
def homepage():
    return 'hello world'
    
if __name__ == '__main__':

    # app.run(debug=True)
    socketIo.run(app)