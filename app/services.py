from .models import Task
from . import db

def criar_tarefa(titulo, descricao, prioridade, user_id):
    tarefa = Task(
        titulo=titulo,
        descricao=descricao,
        prioridade=prioridade,
        user_id=user_id
    )

    db.session.add(tarefa)
    db.session.commit()

    return tarefa

def listar_tarefas(user_id):
    return Task.query.filter_by(user_id=user_id).order_by(Task.status, Task.prioridade).all()

def concluir_tarefa(id):
    tarefa = Task.query.get_or_404(id)

    if tarefa.status != "concluida":
        tarefa.status = "concluida"

    return tarefa


def deletar_tarefa(id):
    tarefa = Task.query.get_or_404(id)

    db.session.delete(tarefa)
    db.session.commit()

