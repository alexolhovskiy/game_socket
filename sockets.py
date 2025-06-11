# sockets.py
from flask import request
from flask_socketio import emit, join_room, leave_room
import time

players = {}

def register_sockets(socketio):
    @socketio.on('connect')
    def on_connect():
        print(f"🟢 Connected: {request.sid}")
        players[request.sid] = {"x": 100, "y": 100}
        emit("players", players, broadcast=True)

    @socketio.on('disconnect')
    def on_disconnect():
        print(f"🔴 Disconnected: {request.sid}")
        players.pop(request.sid, None)
        emit("players", players, broadcast=True)

    @socketio.on("update_player")
    def on_update_player(data):
        players[request.sid] = data  # data = {x: ..., y: ...}
        emit("players", players, broadcast=True)

    # @socketio.on('new_bullet')
    # def handle_new_bullet(data):
    #     emit('new_bullet', data, broadcast=True, include_self=False)


    @socketio.on("new_bullet")
    def on_new_bullet(data):
        data['id'] = f"{request.sid}_b{int(time.time()*1000)}"
        emit("bullets", [data], broadcast=True)