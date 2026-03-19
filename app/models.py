from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from . import db

class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    prioridade = db.Column(db.Integer, nullable=False)  # 1 = alta
    status = db.Column(db.String(20), default="pendente")
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<Task {self.titulo}>"
    
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    tarefas = db.relationship("Task", backref="user", lazy=True)

    def set_password(self, senha):
        self.password = generate_password_hash(senha)

    def check_password(self, senha):
        return check_password_hash(self.password, senha)