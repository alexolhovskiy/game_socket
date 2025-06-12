from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask import Flask
from datetime import timedelta
from flask_socketio import SocketIO





socketio = SocketIO(cors_allowed_origins="*")  # Поддержка CORS для фронта

# 🔹 Создаём экземпляры расширений
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

# 🔹 Функция создания Flask-приложения
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'super-secret'
    app.config['JWT_SECRET_KEY'] = 'jwt-secret'
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=1)

    # Инициализация расширений
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    # CORS(app, supports_credentials=True)
    CORS(app, supports_credentials=True, origins=["http://localhost:5173", "https://your-frontend.onrender.com"])
    socketio.init_app(app)  # 💡 добавляем сюда

    return app
