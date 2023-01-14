
# from threading import Lock
import random
try:
    from __main__ import socketIo
except ImportError:
    from server import socketIo

from flask_socketio import emit
# import requests
# async_mode = None
master_diceList = [] # boardIndex
master_diceHistory = []

# def add_board():
#     master_diceList.append([])
#     master_diceHistory.append([])
@socketIo.on('i_just_connected')
def notify_connection(data):

    emit(f"welcome{data['boardIndex']}", {"diceList": master_diceList, "diceHistory": master_diceHistory})

# @app.route('/diceboard')
# def get_dice_history():
#     return {"history": ["d6:5", "d5:4"]}

@socketIo.on('dice_add')
def handle_add_dice(newDiceData):
    print('\n\n\n\n\n')
    print(newDiceData)
    print('\n\n\n\n\n')
    dicemax = int(newDiceData["dicemax"])

    original_dice = newDiceData["allDice"]
    original_history = newDiceData["allhistory"]

    master_diceList.append([dicemax, f'd{dicemax}', False]) 
    emit(f"get_dice{newDiceData['boardIndex']}", {"history": master_diceHistory, "diceList": master_diceList}, broadcast=True)
    return

@socketIo.on('delete_dice')
def delete_dice(data):
    index = data["index"]
    del master_diceList[index]
    emit(f"get_dice{data['boardIndex']}", {"history": master_diceHistory, "diceList": master_diceList}, broadcast=True)
    return

@socketIo.on('clear_dice')
def clear_dice(data):
    master_diceList.clear()
    print(master_diceList)
    emit(f"get_dice{data['boardIndex']}", {"history": master_diceHistory, "diceList": master_diceList}, broadcast=True)
    return

@socketIo.on('clear_history')
def clear_history(data):
    master_diceHistory.clear()
    emit(f"get_dice{data['boardIndex']}", {"history": master_diceHistory, "diceList": master_diceList}, broadcast=True)
    return

@socketIo.on('i_clicked_roll')
def handle_start_roll(data):
    maxRoll = data["maxRoll"]
    index = data["index"]
    actual_answer = random.randint(1, maxRoll)
    master_diceHistory.append(f'd{maxRoll}: {actual_answer}')
    emit(f"everyone_start_roll{data['boardIndex']}", {"index":index, "predetermined_result": actual_answer}, broadcast=True)

@socketIo.on('dice_update')
def handle_new_roll(newRollData):

    diceval = newRollData["diceval"]
    dicemax = newRollData["dicemax"]
    index = newRollData["index"]

    original_history = newRollData["allhistory"]
    original_dice = newRollData["allDice"]

    master_diceList[index][1] = diceval
    emit(f"get_dice{newRollData['boardIndex']}", {"history": master_diceHistory, "diceList": master_diceList}, broadcast=True)
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
# if __name__ == '__main__':

#     # app.run(debug=True)
#     socketIo.run(app)

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