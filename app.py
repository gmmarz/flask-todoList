from flask import Flask, render_template, redirect, request
from db import tarefas
from utils import get_new_id
from datetime import datetime as dt

app = Flask(__name__)

@app.route('/tarefas', methods=['GET'])
def index():
    return render_template('index.html', tarefas=tarefas)

@app.route('/tarefas', methods=['POST'])
def save():
    form_data = dict(request.form)
    
    tarefa = {
        'id': get_new_id(tarefas),
        'nome': form_data.get('nome'),
        'descricao': form_data.get('descricao'),
        'data_inicio': dt.strptime(form_data.get('data_inicio'), '%Y-%m-%d').date(),
        'data_conclusao': None,
        'concluida': False
    }
    tarefas.append(tarefa)
    
    return redirect('/tarefas')

if __name__ == '__main__':
    app.run(debug=True)