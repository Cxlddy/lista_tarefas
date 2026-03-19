from flask import Blueprint, render_template, request, redirect, url_for, session
from .models import Task, User
from . import db
from .services import(
    criar_tarefa,
    concluir_tarefa,
    listar_tarefas,
    deletar_tarefa
)

main = Blueprint("main", __name__)

@main.route("/")
def home():
    tarefas = listar_tarefas()
    return render_template("index.html", tarefas=tarefas)
    if "user_id" not in session:
        return redirect(url_for("main.login"))

@main.route("/criar", methods=["POST"])
def criar():
    titulo = request.form.get("titulo")
    descricao = request.form.get("descricao")
    prioridade = int(request.form.get("prioridade"))

    criar_tarefa(titulo, descricao, prioridade)
    return redirect(url_for("main.home"))


@main.route("/concluir/<int:id>")
def concluir(id):
    concluir_tarefa(id)
    return redirect(url_for("main.home"))

@main.route("/deletar/<int:id>")
def deletar(id):
    deletar_tarefa(id)
    return redirect(url_for("main.home"))

@main.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        username = request.form.get("username")
        senha = request.form.get("senha")

        user = User(username=username)
        user.set_password(senha)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("main.login"))

    return render_template("registro.html")

@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        senha = request.form.get("senha")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(senha):
            session["user_id"] = user.id
            return redirect(url_for("main.home"))

    return render_template("login.html")

@main.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.login"))