from db import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), unique=True, nullable=False)
    senha = db.Column(db.String(20), nullable=False)
    
    # Relacionamento com Tarefas
    tarefas = db.relationship('Tarefa', backref='usuario', lazy=True)

    def __repr__(self):
        return f"<Usuario {self.nome}>"

class Tarefa(db.Model):
    __tablename__ = 'tarefas'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='pendente')
    data_criacao = db.Column(db.DateTime, nullable=False)
    data_conclusao = db.Column(db.DateTime, nullable=True)
    
    # Chave estrangeira para associar a tarefa a um usuário
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    def __repr__(self):
        return f"<Tarefa {self.titulo} para Usuario ID {self.usuario_id}>"
