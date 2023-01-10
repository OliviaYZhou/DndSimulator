import sqlite3
from threading import Lock
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, send
# import requests
# async_mode = None

app = Flask(__name__)
socketIo = SocketIO(app, cors_allowed_origins="*")

@app.route('/diceboard')
def get_dice_history():
    return {"history": ["d6:5", "d5:4"]}

@socketIo.on('dice_add')
def handle_add_dice(newDiceData):


    dicemax = newDiceData["dicemax"]
    original_dice = newDiceData["allDice"]
    original_history = newDiceData["allhistory"]

    original_dice.append([dicemax, dicemax]) 
    emit("get_dice", {"history": original_history, "diceList": original_dice}, broadcast=True)
    return

@socketIo.on('dice_update')
def handle_new_roll(newRollData):

    diceval = newRollData["diceval"]
    dicemax = newRollData["dicemax"]
    index = newRollData["index"]

    original_history = newRollData["allhistory"]
    original_dice = newRollData["allDice"]

    original_history.append(f'd{dicemax}:{diceval}')
    original_dice[index][1] = diceval
    emit("get_dice", {"history": original_history, "diceList": original_dice}, broadcast=True)
    return


# @app.route('/diceboard/newroll',methods = ['GET', 'POST'])
# def post_new_roll():
#     diceval = request.json["diceval"]
#     dicemax = request.json["dicemax"]
#     index = request.json["index"]

#     original_history = request.json["allhistory"]
#     original_dice = request.json["allDice"]
#     # pretend_original_history = ["d10:9", "d9:8"]
#     # save to db
#     original_history.append(f'd{dicemax}:{diceval}')
#     original_dice[index][1] = diceval
#     return {"history": original_history, "diceList": original_dice}

# Running app
if __name__ == '__main__':
    # app.run(debug=True)
    socketIo.run(app)

# socketio = SocketIO(app, async_mode=async_mode)
# thread = None
# thread_lock = Lock()

# def background_thread():
#     """Example of how to send server generated events to clients."""
#     count = 0
#     while True:
#         socketio.sleep(3)
#         count += 1
#         price = ((requests.get(url)).json())['data']['amount']
#         socketio.emit('my_response',
#                       {'data': 'Bitcoin current price (USD): ' + price, 'count': count})

# @app.route('/')
# def index():
#     return render_template('index.html', async_mode=socketio.async_mode)

# @socketio.event
# def my_event(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': message['data'], 'count': session['receive_count']})

# # Receive the test request from client and send back a test response
# @socketio.on('test_message')
# def handle_message(data):
#     print('received message: ' + str(data))
#     emit('test_response', {'data': 'Test response sent'})

# # Broadcast a message to all clients
# @socketio.on('broadcast_message')
# def handle_broadcast(data):
#     print('received: ' + str(data))
#     emit('broadcast_response', {'data': 'Broadcast sent'}, broadcast=True)

# @socketio.event
# def connect():
#     global thread
#     with thread_lock:
#         if thread is None:
#             thread = socketio.start_background_task(background_thread)
#     emit('my_response', {'data': 'Connected', 'count': 0})

# if __name__ == '__main__':
#     socketio.run(app)