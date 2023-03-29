try:
    from __main__ import socketIo, app #, api
except ImportError:
    from server import socketIo, app #, api
from flask_socketio import emit
from flask import request
from backend.server_functions import *


import database.character_db as character_db

@app.route('/api/get_all_characters')
def send_character_id_list():
    all_ids = character_db.get_character_id_list()
    return {"character_master_list": all_ids}

@app.route('/api/character_connected/') #?characterid=<characterid>
def send_all_stats():
    # print("api send_all_stats")
    characterid = request.args.get('characterid')
    basic_character_info = character_db.get_basic_character(characterid)
    
    if basic_character_info["character_type"] == "basic":
        return basic_character_info
    else:
        print_block(basic_character_info, "basic_character_info")
        all_stats = character_db.get_all_player_info(characterid)
        if not all_stats:
            return basic_character_info
        # print(all_stats, "api\n\n\n\n")
        return all_stats
    return default_return

@app.route('/api/status_effect/', methods=["GET", "POST"]) #?characterid=<characterid>
def add_status_effect():
    data = request.json
    print("api add_status_effect")
    character_db.add_status_effect(data["characterid"], data["name"], data["stats"], data["duration"], data["description"])
    character_db.save_db(charid=data["characterid"])
    # print(character_db.get_player_stats(data["characterid"]))
    socketIo.emit(f"get_character_changes/{data['characterid']}", character_db.get_player_stats(data["characterid"]))
    return default_return

@app.route('/api/add_character/', methods=["GET", "POST"])
def add_basic_character():
    data = request.form
    print_block(data, "form")
    character_db.add_character(data["characterid"], data["characterName"], data["characterType"])
    print_block(character_db.get_character_id_list())
    socketIo.emit(f"master_character_changes", {"master_character_list": character_db.get_character_id_list()})
    return default_return

@app.route('/api/add_new_stats/', methods=["GET", "POST"])
def add_new_stats():
    data = request.form
    # print_block(data, "form")
    stat_str = f"{data['HP']} {data['STR']} {data['DEX']} {data['CON']} {data['INT']} {data['WIS']} {data['CHA']}"
    print_block((data["characterid"], stat_str, data['level']), "newstats")
    # return {"b": True}
    character_db.add_character_stats(data["characterid"], stat_str, data['level'])
    socketIo.emit(f"get_character_changes/{data['characterid']}", character_db.get_player_stats(data["characterid"]))
    return default_return

@app.route('/api/add_new_cumulative_stats/', methods=["GET", "POST"])
def add_new_cumulative_stats():
    data = request.form
    print_block(data, "form")
    character_db.add_cumulative_stats(data["characterid"], data["gold"], data["exp"])
    
    socketIo.emit(f"get_character_changes/{data['characterid']}", character_db.get_player_stats(data["characterid"]))
    return default_return

@app.route('/api/add_permanent_effect/', methods=["GET", "POST"])
def add_permanent_effect():
    data = request.form
    print_block(data, "form")
    if (data["effect-type"] == "Gold"):
        character_db.update_gold(data["characterid"], data["effect-amount"])
    if (data["effect-type"] == "Exp"):
        character_db.update_exp(data["characterid"], data["effect-amount"])
    if (data["effect-type"] == "Level"):
        character_db.update_level(data["characterid"], data["effect-amount"])
    if (data["effect-type"] == "HP"):
        pass
    socketIo.emit(f"get_character_changes/{data['characterid']}", character_db.get_player_stats(data["characterid"]))
    return default_return

@app.route('/api/add_inventory_item/', methods=["GET", "POST"])
def add_inventory_item():
    data = request.form
    print_block(data, "form")
    character_db.add_inventory_item(data["characterid"], data["item-name"], data["amount"])
    socketIo.emit(f"get_character_changes/{data['characterid']}", character_db.get_character_inventory(data["characterid"]))
    return default_return

@app.route('/api/delete_character/', methods=["DELETE", "POST"])
def delete_character():
    characterid = request.args.get('characterid')
    print_block(characterid, "delete character")
    character_db.delete_character(characterid)
    print_block(character_db.get_character_id_list())
    socketIo.emit(f"master_character_changes", {"master_character_list": character_db.get_character_id_list()})
    return default_return

@app.route('/api/delete_status_effect/', methods=["DELETE", "POST"])
def delete_status_effect():
    characterid = request.args.get('characterid')
    effect_name = request.args.get('effect_name')
    print_block(characterid, f"delete status_effect {effect_name}")
    character_db.delete_status_effect(characterid, effect_name)

    socketIo.emit(f"get_character_changes/{characterid}", character_db.get_player_stats(characterid))
    return default_return

@app.route('/api/delete_inventory_item/', methods=["DELETE", "POST"])
def delete_inventory_item():
    characterid = request.args.get('characterid')
    item_name = request.args.get('item_name')
    print_block(characterid, f"delete inventory_item {item_name}")
    character_db.remove_inventory_item(characterid, item_name, 1)

    socketIo.emit(f"get_character_changes/{characterid}", character_db.get_character_inventory(characterid))
    return default_return
# @socketIo.on('character_connected')
# def send_all_stats(data):
#     print("server js\n\n\n\n")
#     characterid = data["characterid"]
#     all_stats = character_db.get_player_stats(characterid)
#     socketIo.emit("character_setup", all_stats)


# @socketIo.on("/status_effect/")
# def add_status_effect(data):
#     print("add_status_effect", data)
#     character_db.add_status_effect(data["characterid"], data["name"], data["stats"], data["duration"], data["description"])
#     character_db.save_db(charid=data["characterid"])
#     # print(character_db.get_player_stats(data["characterid"]))
#     socketIo.emit(f"get_character_changes/{data['characterid']}", character_db.get_player_stats(data["characterid"]))
#     return {"b": True}


# @socketIo.on('character_connected')
# def send_all_stats(data):
#     characterid = data.get('characterid')
#     all_stats = character_db.get_player_stats(characterid)
#     print_block(all_stats, "all_stats")
#     emit(f"character_setup/{characterid}", all_stats)
#     return all_stats
