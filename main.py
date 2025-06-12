from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from sockets import register_sockets

app = Flask(__name__)
CORS(app)  # Разрешаем CORS
app.config['SECRET_KEY'] = 'secret!'

# Используем eventlet, так как Replit его нормально поддерживает
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@app.route('/')
def index():
    return "🎮 Socket.IO сервер работает!"

# Подключаем сокеты
register_sockets(socketio)

# Запускаем
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3000)
