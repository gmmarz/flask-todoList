from flask import Blueprint,render_template, request,redirect
from app.db import tarefas
from app.utils import get_new_id
from datetime import datetime as dt

# Essa blueprint se comporta exatamente como o app
task_bp = Blueprint("Tarefas", __name__, url_prefix="/tarefas")


@task_bp.route("/", methods=["GET"])
def index():
    return render_template("index.html", tarefas=tarefas)


@task_bp.route("/", methods=["POST"])
def save():
    form_data = dict(request.form)

    tarefa = {
        "id": get_new_id(tarefas),
        "nome": form_data.get("nome"),
        "descricao": form_data.get("descricao"),
        "data_inicio": dt.strptime(form_data.get("data_inicio"), "%Y-%m-%d").date(),
        "data_conclusao": None,
        "concluida": False,
    }
    tarefas.append(tarefa)

    return redirect("/tarefas")

@task_bp.route('/<int: id>/delete', methods=['GET'])
def delete(id:int):
    for i, tarefa in enumerate(tarefas):
        if tarefa.get('id') == id:
            tarefas.pop(i)
            return redirect('/tarefas')
