# sockets.py
from flask import request
from flask_socketio import emit, join_room, leave_room
import time
import random

players = {}

def register_sockets(socketio):
    @socketio.on('connect')
    def on_connect():
        print(f"🟢 Connected: {request.sid}")
        players[request.sid] = {"x": 100, "y": 100, "ang": 0,"color":f"rgb({random.randint(0,250)},{random.randint(0,250)},{random.randint(0,250)})"}
        emit("players", players, broadcast=True)
        emit("your_id", request.sid)

    @socketio.on('disconnect')
    def on_disconnect():
        print(f"🔴 Disconnected: {request.sid}")
        players.pop(request.sid, None)
        emit("players", players, broadcast=True)

    @socketio.on("update_player")
    def on_update_player(data):
        players[request.sid] = data  # data = {x: ..., y: ...}
        emit("players", players, broadcast=True)

    @socketio.on("new_bullet")
    def on_new_bullet(data):
        data['id'] = f"{request.sid}_b{int(time.time()*1000)}"
        emit("bullets", [data], broadcast=True)


# from flask_jwt_extended import decode_token
# from models import User
# from flask import request
# from flask_socketio import emit, disconnect,join_room, leave_room
# import time
# from extensions import db
# from models import User


# players = {}

# def register_sockets(socketio):

#     @socketio.on('connect')
#     def on_connect(auth):
#         print(f"[SOCKET CONNECT] SID: {request.sid}, AUTH: {auth}")

#         token = auth.get("token") if auth else None
#         if not token:
#             print("[SOCKET] ❌ Нет токена")
#             return disconnect()

#         try:
#             decoded = decode_token(token)
#             user_id = decoded["sub"]  # или "identity" — зависит от настройки JWT
#             user = db.session.get(User, user_id)

#             if not user:
#                 print("[SOCKET] ❌ Пользователь не найден")
#                 return disconnect()

#         except Exception as e:
#             print("[SOCKET] ❌ Ошибка при разборе токена:", str(e))
#             return disconnect()

#         # ✅ Всё ок, добавляем игрока
#         players[request.sid] = {
#             "x": 100, "y": 100, "ang": 0,
#             "username": user.username,
#             "color": user.color,
#             "id": user.id
#         }

#         emit("your_id", request.sid)
#         emit("players", players, broadcast=True)
#         print(f"[SOCKET] ✅ Подключился: {user.username} (id: {user.id})")

#     @socketio.on('disconnect')
#     def on_disconnect():
#         print(f"🔴 Отключился: {request.sid}")
#         players.pop(request.sid, None)
#         emit("players", players, broadcast=True)

#     @socketio.on("update_player")
#     def on_update_player(data):
#         if request.sid in players:
#             players[request.sid].update(data)
#         emit("players", players, broadcast=True)

#     @socketio.on("new_bullet")
#     def on_new_bullet(data):
#         data['id'] = f"{request.sid}_b{int(time.time()*1000)}"
#         emit("bullets", [data], broadcast=True)
