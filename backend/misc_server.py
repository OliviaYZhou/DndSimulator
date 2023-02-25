try:
    from __main__ import socketIo, app #, api
except ImportError:
    from server import socketIo, app #, api
from flask_socketio import emit
from flask import request
from backend.server_functions import *

time_hour = 0
time_minute = 0

@socketIo.on('change_time')
def change_time(hour, minute):
    global time_hour
    global time_minute
    time_hour = hour
    time_minute = minute
    emit(f"get_time_input", {"hour": hour, "minute": minute})