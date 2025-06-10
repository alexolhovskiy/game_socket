# sockets.py
from flask import request
from flask_socketio import emit, join_room, leave_room

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
