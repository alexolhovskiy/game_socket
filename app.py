from extensions import create_app, db, socketio
from models import User
from routes import register_routes
from sockets import register_sockets  # ⬅️ создадим этот файл сейчас
import os

app = create_app()
register_routes(app)
register_sockets(socketio)  # 💡 подключаем обработчики WebSocket

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # socketio.run(app, debug=True)  # ⬅️ запускаем через socketio
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
