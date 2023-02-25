
# from threading import Lock
import random
try:
    from __main__ import socketIo, app 
except ImportError:
    from server import socketIo, app 

from flask_socketio import emit
from flask import request
from backend.server_functions import *
# import requests
# async_mode = None
master_diceList = [] # boardIndex
# master_diceList_index
master_diceHistory = []

# initial_dice_boards = ["tentacle_guy", "orc_guy", "Enemy", "npc1", "npc2"]
master_diceDict = {}
master_diceHistoryDict = {}


@socketIo.on('i_just_connected')
def notify_connection(data):
    board_id = data["boardId"]
    print("\n\n\nconnect board\n\n\n", board_id)
    # if board_index > len(master_diceList)-1:
    #     master_diceList.append([])
    #     master_diceHistory.append([])
    if board_id not in master_diceDict:
        print(f"\n\n\nError, board {board_id} not in master dice list")
        master_diceDict[board_id] = []
        master_diceHistoryDict[board_id] = []
        print(f"Board {board_id} added to master dice list")
        print(f"MasterDiceDict\n {master_diceDict}\n\n\n")

    # emit(f"welcome/{board_index}", {"diceList": master_diceList[board_index], "diceHistory": master_diceHistory[board_index]})
    emit(f"welcome/{board_id}", {"diceList": master_diceDict[board_id], "diceHistory": master_diceHistoryDict[board_id]})

@socketIo.on('dice_add')
def handle_add_dice(newDiceData):
    # print('\n\n\n\n\n')
    # print("server add dice", newDiceData)
    # print('\n\n\n\n\n')
    # board_index = int(newDiceData["boardIndex"])

    board_id = newDiceData["boardId"]
    print("\n\n\nadd dice boardid\n\n\n", board_id)
    dicemax = int(newDiceData["dicemax"])
    
    print('\n\n\n\n\n')
    print("server add dice", master_diceList)
    print('\n\n\n\n\n')
    # master_diceList[board_index].append([dicemax, f'd{dicemax}', False]) 
    master_diceDict[board_id].append([dicemax, f'd{dicemax}', False]) 
    # emit(f"get_dice/{newDiceData['boardIndex']}", {"history": master_diceHistory[board_index], "diceList": master_diceList[board_index]}, broadcast=True)
    emit(f"get_dice/{newDiceData['boardId']}", {"history": master_diceHistoryDict[board_id], "diceList": master_diceDict[board_id]}, broadcast=True)
    return

@socketIo.on('delete_dice')
def delete_dice(data):
    board_id = data["boardId"]

    index = data["index"]
    del master_diceDict[board_id][index]
    emit(f"get_dice/{data['boardId']}", {"history": master_diceHistoryDict[board_id], "diceList": master_diceDict[board_id]}, broadcast=True)
    return

@socketIo.on('clear_dice')
def clear_dice(data):
  
    board_id = data["boardId"]
    
    master_diceDict[board_id].clear()
    # print(master_diceList)
    emit(f"get_dice/{data['boardId']}", {"history": master_diceHistoryDict[board_id], "diceList": master_diceDict[board_id]}, broadcast=True)
    return

@socketIo.on('clear_history')
def clear_history(data):

    board_id = data["boardId"]
    master_diceHistoryDict[board_id].clear()
    emit(f"get_dice/{data['boardId']}", {"history": master_diceHistoryDict[board_id], "diceList": master_diceDict[board_id]}, broadcast=True)
    return

@socketIo.on('i_clicked_roll')
def handle_start_roll(data):

    board_id = data["boardId"]
    maxRoll = data["maxRoll"]
    index = data["index"]
    actual_answer = random.randint(1, maxRoll)
    master_diceHistoryDict[board_id].append(f'd{maxRoll}: {actual_answer}')
    emit(f"everyone_start_roll/{data['boardId']}", {"index":index, "predetermined_result": actual_answer}, broadcast=True)

@socketIo.on('dice_update')
def handle_new_roll(newRollData):
    print(f"{master_diceDict}")

    board_id = newRollData["boardId"]
    diceval = newRollData["diceval"]
    index = newRollData["index"]

    # original_history = newRollData["allhistory"]
    # original_dice = newRollData["allDice"]

    master_diceDict[board_id][index][1] = diceval
    emit(f"get_dice/{newRollData['boardId']}", {"history": master_diceHistoryDict[board_id], "diceList": master_diceDict[board_id]}, broadcast=True)
    return

@app.route("/api/get_master_dice")
def get_master_dice():
    # if not master_diceDict:
    #     return {"dice_boards": initial_dice_boards}
    # else:
    return {"dice_boards": [key for key in master_diceDict]}

@app.route("/api/add_new_diceboard/", methods=["GET", "POST"])
def add_new_diceboard():
    data = request.form
    print("\n\n\nadd new diceboard\n\n\n", data)
    board_id = data["boardId"]
    if board_id not in master_diceDict:
        master_diceDict[board_id] = []
        master_diceHistoryDict[board_id] = []
    socketIo.emit("get_new_diceboard", {"boardId": board_id})
    return default_return

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