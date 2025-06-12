# # sockets.py
# from flask import request
# from flask_socketio import emit, join_room, leave_room
# import time

# players = {}

# def register_sockets(socketio):
#     @socketio.on('connect')
#     def on_connect():
#         print(f"🟢 Connected: {request.sid}")
#         players[request.sid] = {"x": 100, "y": 100, "ang": 0}
#         emit("players", players, broadcast=True)
#         emit("your_id", request.sid)

#     @socketio.on('disconnect')
#     def on_disconnect():
#         print(f"🔴 Disconnected: {request.sid}")
#         players.pop(request.sid, None)
#         emit("players", players, broadcast=True)

#     @socketio.on("update_player")
#     def on_update_player(data):
#         players[request.sid] = data  # data = {x: ..., y: ...}
#         emit("players", players, broadcast=True)

#     @socketio.on("new_bullet")
#     def on_new_bullet(data):
#         data['id'] = f"{request.sid}_b{int(time.time()*1000)}"
#         emit("bullets", [data], broadcast=True)


from flask_jwt_extended import decode_token
from flask_socketio import disconnect
from models import User
from flask import request

players = {}

def register_sockets(socketio):

    @socketio.on('connect')
    def on_connect(auth):
        print(f"🟢 Подключение: {request.sid}")
        
        token = auth.get('token') if auth else None
        if not token:
            print("⛔ Нет токена! Отключаем.")
            return disconnect()

        try:
            decoded = decode_token(token)
            user_id = decoded['sub']
            user = User.query.get(user_id)
            if not user:
                print("⛔ Пользователь не найден.")
                return disconnect()

            print(f"✅ Пользователь {user.username} вошёл в игру.")

            # Добавляем игрока
            players[request.sid] = {
                "x": 100,
                "y": 100,
                "ang": 0,
                "username": user.username,
                "color": user.color,
                "id": user.id
            }

            emit("players", players, broadcast=True)
            emit("your_id", request.sid)

        except Exception as e:
            print("⛔ Ошибка при проверке токена:", str(e))
            return disconnect()

    @socketio.on('disconnect')
    def on_disconnect():
        print(f"🔴 Отключился: {request.sid}")
        players.pop(request.sid, None)
        emit("players", players, broadcast=True)

    @socketio.on("update_player")
    def on_update_player(data):
        if request.sid in players:
            players[request.sid].update(data)
        emit("players", players, broadcast=True)

    @socketio.on("new_bullet")
    def on_new_bullet(data):
        data['id'] = f"{request.sid}_b{int(time.time()*1000)}"
        emit("bullets", [data], broadcast=True)
