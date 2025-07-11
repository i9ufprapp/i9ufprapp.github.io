from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    setor_id = db.Column(db.Integer, db.ForeignKey('setor.id'), nullable=True)
    senha = db.Column(db.String(200), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    bolsista = db.Column(db.Boolean, default=False)
    admin = db.Column(db.Boolean, default=False)
    ano_entrada = db.Column(db.Integer, nullable=False)
    linkedin = db.Column(db.String(200))
    preferencia = db.Column(db.String(60), nullable=False)
    wats = db.Column(db.String(20))
    horas_semana = db.Column(db.String(20))
    image_path = db.Column(db.String(255))

class Projeto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255))
    responsavel = db.Column(db.String(255))
    image_path = db.Column(db.String(255))

class Setor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255))
    projeto_id = db.Column(db.Integer, db.ForeignKey('projeto.id'))
    image_path = db.Column(db.String(255))

class Atividade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    setor_id = db.Column(db.Integer, db.ForeignKey('setor.id'))
    descricao = db.Column(db.String(255), nullable=False)
    data_inicio = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    data_fim_previsto = db.Column(db.DateTime, nullable=False)
    data_fim_real = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), default='Pendente')
    nivel = db.Column(db.String(150), default='normal')
    image_path = db.Column(db.String(255))

class Atividadealuno(db.Model):
    atividade_id = db.Column(db.Integer, db.ForeignKey('atividade.id'), primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'), primary_key=True)

def init_db(app):
    """Função para inicializar o banco de dados e criar tabelas"""
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Este comando cria todas as tabelas definidas nos modelos
        print("✅ Tabelas criadas com sucesso!")






        