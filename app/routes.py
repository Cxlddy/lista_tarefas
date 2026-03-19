from flask import Blueprint, render_template, request, redirect, url_for, session
from .models import db, Task, User

main = Blueprint("main", __name__)


# 🔹 HOME (PROTEGIDA)
@main.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    tarefas = Task.query.filter_by(user_id=session["user_id"]).order_by(Task.prioridade).all()
    return render_template("index.html", tarefas=tarefas)


# 🔹 LOGIN
@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        senha = request.form["senha"]

        user = User.query.filter_by(username=username, senha=senha).first()

        if user:
            session["user_id"] = user.id
            return redirect(url_for("main.home"))

    return render_template("login.html")


# 🔹 REGISTRO
@main.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        username = request.form["username"]
        senha = request.form["senha"]

        user_existente = User.query.filter_by(username=username).first()

        if user_existente:
            return "Usuário já existe"

        novo_user = User(username=username, senha=senha)
        db.session.add(novo_user)
        db.session.commit()

        return redirect(url_for("main.login"))

    return render_template("registro.html")


# 🔹 LOGOUT
@main.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.login"))


# 🔹 CRIAR TAREFA
@main.route("/criar", methods=["POST"])
def criar():
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    titulo = request.form["titulo"]
    descricao = request.form["descricao"]
    prioridade = request.form["prioridade"]

    nova = Task(
        titulo=titulo,
        descricao=descricao,
        prioridade=prioridade,
        user_id=session["user_id"]
    )

    db.session.add(nova)
    db.session.commit()

    return redirect(url_for("main.home"))


# 🔹 CONCLUIR
@main.route("/concluir/<int:id>")
def concluir(id):
    tarefa = Task.query.get(id)

    if tarefa and tarefa.user_id == session.get("user_id"):
        tarefa.status = "concluida"
        db.session.commit()

    return redirect(url_for("main.home"))


# 🔹 DELETAR
@main.route("/deletar/<int:id>")
def deletar(id):
    tarefa = Task.query.get(id)

    if tarefa and tarefa.user_id == session.get("user_id"):
        db.session.delete(tarefa)
        db.session.commit()

    return redirect(url_for("main.home"))