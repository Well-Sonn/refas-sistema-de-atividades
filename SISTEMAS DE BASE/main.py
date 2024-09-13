from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import datetime
from models import Usuario, Tarefa
from db import db

app = Flask(__name__)
app.config['SECRET_KEY'] = "PALAVRA-SECRETA"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubanco.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route("/")
def home():
    return render_template("html/login.html")

@app.route("/login", methods=['POST'])
def login():
    usuario_nome = request.form.get('nome')
    senha = request.form.get('senha')
    usuario = Usuario.query.filter_by(nome=usuario_nome, senha=senha).first()

    if usuario:
        return redirect(url_for('acesso', nome=usuario.nome))
    else:
        flash('Usuário ou senha inválidos')
        return redirect("/")

@app.route("/cadastrar")
def cadastrar():
    return render_template("html/cadastrar.html")

@app.route("/processar_cadastro", methods=['POST'])
def processar_cadastro():
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    confirmar_senha = request.form.get('confirmar_senha')
    
    if senha != confirmar_senha:
        flash('As senhas não coincidem')
        return redirect('/cadastrar')
    
    usuario_existente = Usuario.query.filter_by(nome=nome).first()
    if usuario_existente:
        flash('Usuário já cadastrado')
        return redirect('/cadastrar')
    
    novo_usuario = Usuario(nome=nome, senha=senha)
    db.session.add(novo_usuario)
    db.session.commit()
    
    flash('Usuário cadastrado com sucesso')
    return redirect("/")

@app.route("/acesso")
def acesso():
    nome_usuario = request.args.get('nome')
    usuario = Usuario.query.filter_by(nome=nome_usuario).first()
    if not usuario:
        flash('Usuário não encontrado')
        return redirect("/")

    tarefas_usuario = usuario.tarefas
    return render_template("html/acesso.html", nomeUsuario=usuario.nome, tarefas=tarefas_usuario)


@app.route("/criar_tarefa/<string:usuario_id>", methods=['GET', 'POST'])
def criar_tarefa(usuario_id):
    usuario = Usuario.query.filter_by(nome=usuario_id).first()
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        nova_tarefa = Tarefa(
            titulo=titulo,
            descricao=descricao,
            status='pendente',
            data_criacao=datetime.now(),
            usuario=usuario
        )
        db.session.add(nova_tarefa)
        db.session.commit()
        return redirect(url_for('acesso', nome=usuario.nome))

    return render_template('html/criar_tarefa.html', usuario=usuario)

@app.route("/editar_tarefa/<int:tarefa_id>", methods=['GET', 'POST'])
def editar_tarefa(tarefa_id):
    tarefa = Tarefa.query.get_or_404(tarefa_id)
    if request.method == 'POST':
        tarefa.titulo = request.form.get('titulo')
        tarefa.descricao = request.form.get('descricao')
        tarefa.status = request.form.get('status')
        tarefa.data_conclusao = datetime.now() if tarefa.status == 'CONCLUÍDA' else None
        db.session.commit()
        return redirect(url_for('acesso', nome=tarefa.usuario.nome))

    return render_template('html/editar_tarefa.html', tarefa=tarefa)

@app.route("/excluir_tarefa/<int:tarefa_id>", methods=['POST'])
def excluir_tarefa(tarefa_id):
    tarefa = Tarefa.query.get_or_404(tarefa_id)
    usuario = tarefa.usuario  
    db.session.delete(tarefa)
    db.session.commit()
    return redirect(url_for('acesso', nome=usuario.nome))


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)