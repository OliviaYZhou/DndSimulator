try:
    from __main__ import socketIo, app, api
except ImportError:
    from server import socketIo, app, api

from flask import request

import database.character_db as character_db

@app.route('/character_connected/') #?characterid=<characterid>
def send_all_stats():
    print("\n\n\n\n\n\n something")
    characterid = request.args.get('characterid')
    all_stats = character_db.get_player_stats(characterid)
    # print(all_stats, "\n\n\n\n")
    return all_stats

# @socketIo.on('character_connected')
# def send_all_stats(data):
#     print("server js\n\n\n\n")
#     characterid = data["characterid"]
#     all_stats = character_db.get_player_stats(characterid)
#     socketIo.emit("character_setup", all_stats)


