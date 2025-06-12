from flask import request, jsonify
from extensions import db, bcrypt
from models import User
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)

def register_routes(app):
    @app.route("/api/hello")
    def hello():
        return jsonify({"message": "Привет от Flask!"})
       
    @app.route('/api/refresh', methods=['POST'])
    @jwt_required(refresh=True)
    def refresh():
        identity = get_jwt_identity()
        new_access_token = create_access_token(identity=identity)
        return jsonify(access_token=new_access_token)

    @app.route('/api/register', methods=['POST'])
    def register():
        data = request.get_json()
        print("Пришло:", data)

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        r_password = data.get('r_password')
        color = data.get('color')

        print("username:", username)
        print("email:", email)
        print("password:", password)
        print("r_password:", r_password)
        print("color:", color)

        if not all([username, email, password, r_password]):
            print("⛔ Проблема: не все поля пришли")
            return jsonify({'error': 'Missing fields'}), 400

        if password != r_password:
            print("⛔ Проблема: пароли не совпадают")
            return jsonify({'error': 'Passwords do not match'}), 400

        if User.query.filter_by(email=email).first():
            print("⛔ Проблема: пользователь уже существует")
            return jsonify({'error': 'User already exists'}), 400

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_pw, color=color)
        db.session.add(new_user)
        db.session.commit()

        print("✅ Регистрация успешна")
        return jsonify({'message': 'Registration OK'})


    @app.route('/api/login', methods=['POST'])
    def login():
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        # 💥 проверка пустых полей
        if not email or not password:
            return jsonify({"error": "Missing email or password"}), 400

        user = User.query.filter_by(email=email).first()

        if not user or not bcrypt.check_password_hash(user.password, password):
            return jsonify({"error": "Invalid credentials"}), 401

        access = create_access_token(identity=user.id)
        refresh = create_refresh_token(identity=user.id)
        return jsonify(access_token=access, refresh_token=refresh), 200
    
    @app.route('/api/protected')
    @jwt_required()
    def protected():
        user_id = get_jwt_identity()
        print('🔍 user_id:', user_id)  # <-- вот это добавь
        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "color": user.color,
            "score": user.score,
    })