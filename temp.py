# run.py или app.py
from extensions import db, create_app
from models import User

app = create_app()

with app.app_context():
    db.create_all()  # 💥 Создаст таблицы, если их нет