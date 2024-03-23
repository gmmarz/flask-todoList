import os
import flask_login as fl
from datetime import datetime as dt
from flask import Flask, render_template, redirect, request, flash
from db import db, migrate
from models import Tarefa, User
from dotenv import load_dotenv

from auth import login_manager


app = Flask(__name__)

load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


# View Routes
@app.route("/", methods=["GET"])
def root():
    return redirect('/tarefas/listar')

@app.route("/login", methods=["GET"])
def login():
    return render_template('user/login.html')

@app.route("/registrar", methods=["GET"])
def register():
    return render_template('user/register.html')


@app.route("/tarefas/listar", methods=["GET"])
@fl.login_required
def index():
    
    user:User = fl.current_user
    
    tarefas = db.session.query(Tarefa)\
        .where(Tarefa.user_id == user.id ).all()
    return render_template("tarefa/index.html", tarefas=tarefas)

@app.route('/tarefas/criar', methods=['GET'])
@fl.login_required
def create():
    return render_template("tarefa/create.html")

@app.route('/tarefas/<int:id>/editar', methods=['GET'])
@fl.login_required
def edit(id: int):
    tarefa = db.session.query(Tarefa).get(id)
    return render_template("tarefa/edit.html", tarefa=tarefa)

# Action Routes
# Função que irá executar o login
@app.route("/login", methods=['POST'])
def login_user():
    form_data = dict(request.form)

    nome = form_data.get('nome')
    senha = form_data.get('senha')
    lembrar = form_data.get('lembrar')

    user = db.session.query(User)\
        .where(User.nome == nome).first()
    
    if user is None or not user.verificar_senha(senha):
        flash('Credenciais Inválidas.', category='error')
        return redirect('/login')

	# Executando a função de login do flask login
    fl.login_user(user, remember=lembrar)
    return redirect('/tarefas/listar')

# Funçao que irá realizar o logout
# A função login required diz que essa rota só pode ser acessada por quem estiver logado

@app.route("/logout", methods=["GET"])
@fl.login_required
def logout():
	# Desloga o usuário logado
    fl.logout_user()
    return redirect('/login')

@app.route('/registrar', methods=["POST"])
def save_user():
    form_data = dict(request.form)

    nome = form_data.get('nome')
    senha = form_data.get('senha')
    confirmar_senha = form_data.get('confirmar-senha')

	# Validação de criação de senha
    if senha != confirmar_senha:
        flash('As senhas não batem.', category='error')
        return redirect('/registrar')

	# Validação de usuário existente
    user_exists = db.session.query(User)\
        .where(User.nome == nome).first()
        
    if user_exists:
        flash('Usuário já existente', category='error')
        return redirect('/registrar')
		
	# Criando usuário
    user = User(nome, senha)
    
    # Persistindo no banco de dados
    db.session.add(user)
    db.session.commit()

    flash('Usuário cadastrado com sucesso.', category='success')
    return redirect('/login')


@app.route("/tarefas/save", methods=["POST"])
def save():
    user:User = fl.current_user
    form_data = dict(request.form)
    
    tarefa = Tarefa(
        form_data.get("nome"),
        form_data.get("descricao"),
        dt.strptime(form_data.get("data_inicio"), "%Y-%m-%d").date(),
        form_data.get("data_conclusao")
    )
    db.session.add(tarefa)
    db.session.commit()
    
    return redirect("/tarefas/listar")

@app.route("/tarefas/update", methods=["POST"])
@fl.login_required
def update():
    form_data = dict(request.form)
    
    id = form_data.get('id')
    tarefa_db: Tarefa = db.session.query(Tarefa).get(id)
    
    tarefa_db.update(form_data)
    db.session.commit()
    
    return redirect("/tarefas/listar")


@app.route("/tarefas/<int:id>/delete", methods=["GET"])
@fl.login_required
def delete(id: int):
    tarefa = db.session.query(Tarefa).get(id)
    
    db.session.delete(tarefa)
    db.session.commit()

    return redirect("/tarefas/listar")

with app.app_context():
    db.init_app(app)
    migrate.init_app(app)
    login_manager.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
