try:
    from __main__ import socketIo, app, api
except ImportError:
    from server import socketIo, app, api
from flask_socketio import emit
from flask import request

import database.character_db as character_db
@socketIo.on('character_connected')
def send_all_stats(data):
    characterid = data.get('characterid')
    all_stats = character_db.get_player_stats(characterid)
    # print(all_stats, "\n\n\n\n")
    emit(f"character_setup/{characterid}", all_stats)
    return all_stats
# @app.route('/api/character_connected/') #?characterid=<characterid>
# def send_all_stats():
#     characterid = request.args.get('characterid')
#     all_stats = character_db.get_player_stats(characterid)
#     # print(all_stats, "\n\n\n\n")
#     return all_stats

@socketIo.on("/status_effect/")
def add_status_effect(data):
    character_db.add_status_effect(data["characterid"], data["name"], data["stats"], data["duration"], data["description"])
    character_db.save_db(charid=data["characterid"])
    # print(character_db.get_player_stats(data["characterid"]))
    socketIo.emit(f"get_character_changes/{data['characterid']}", character_db.get_player_stats(data["characterid"]))
    return {"b": True}


# @app.route('/api/status_effect/', methods=["GET", "POST"]) #?characterid=<characterid>
# def add_status_effect():
#     data = request.json
#     # print(data["characterid"])
#     character_db.add_status_effect(data["characterid"], data["name"], data["stats"], data["duration"], data["description"])
#     character_db.save_db(charid=data["characterid"])
#     # print(character_db.get_player_stats(data["characterid"]))
#     socketIo.emit(f"get_character_changes/{data['characterid']}", character_db.get_player_stats(data["characterid"]))
#     return {"b": True}


# @socketIo.on('character_connected')
# def send_all_stats(data):
#     print("server js\n\n\n\n")
#     characterid = data["characterid"]
#     all_stats = character_db.get_player_stats(characterid)
#     socketIo.emit("character_setup", all_stats)


