try:
    from __main__ import socketIo
except ImportError:
    from server import socketIo

import character_db

@socketIo.on('character_connected')
def send_all_stats(data):
    print("server js\n\n\n\n")
    characterid = data["characterid"]
    all_stats = character_db.get_player_stats(characterid)
    socketIo.emit("character_setup", all_stats)


