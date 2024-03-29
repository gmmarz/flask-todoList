from datetime import datetime as dt
from flask import Flask, render_template, redirect, request
from db import db, migrate,DATABASE_URI
from models import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI #URL para o flask_sqlAlchemy


# View Routes
@app.route("/", methods=["GET"])
def root():
    return redirect("/tarefas/listar")

@app.route("/tarefas/listar", methods=["GET"])
def index():
    tarefas = db.session.query(Tarefa).all()
    return render_template("index.html", tarefas=tarefas)

@app.route('/tarefas/criar', methods=['GET'])
def create():
    return render_template("create.html")

@app.route('/tarefas/<int:id>/edit', methods=["GET"])
def edit(id:int):
    tarefa = db.session.query(Tarefa).get(id)
    return render_template("edit.html", tarefa = tarefa)

# Action Routes
@app.route("/tarefas/save", methods=["POST"])
def save():
    form_data = dict(request.form)

    tarefa = Tarefa(
       form_data.get("nome"), 
       form_data.get("descricao"),
       dt.strptime(form_data.get("data_inicio"), "%Y-%m-%d").date(),
       form_data.get("data_conclusao"),
    )

    db.session.add(tarefa)
    db.session.commit()

    return redirect("/tarefas/listar")

@app.route("/tarefas/<int:id>/update", methods=["POST"])
def update():
    form_data = dict(request.form)
    id = form_data.get('id')
    tarefa_db:Tarefa = db.session.query(Tarefa).get(id)
    tarefa_db.update(form_data)
    db.session.commit()


@app.route("/tarefas/<int:id>/delete", methods=["GET"])
def delete(id: int):
    
    tarefa = db.session.query(Tarefa).get(id)
    db.session.delete(tarefa)
    db.session.commit()
    
    return redirect("/tarefas/listar")
 
    

#Uma boa pratica para organizar o projeto.
with app.app_context():
    db.init_app(app)
    migrate.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
