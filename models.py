from db import db
from flask_login import UserMixin
from datetime import datetime

class Usuario(UserMixin, db.Model):
    __tablename__ = "Usuario"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)

    cpf_cnpj = db.Column(db.String(20), unique=True)
    celular = db.Column(db.String(20))
    genero = db.Column(db.String(20))
    cidade = db.Column(db.String(50))
    estado = db.Column(db.String(2))
    data_nascimento = db.Column(db.String(10))

    tipo_usuario = db.Column(db.String(20), default='cliente')
    imagem_perfil = db.Column(db.Text)

    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)

class Produto(UserMixin, db.Model):
    __tablename__ = "Produto"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    imagem_id = db.Column(db.Integer,db.ForeignKey('ImagemProduto.id'))
    descricao = db.Column(db.Text)
    marca_id = db.Column(db.Integer, db.ForeignKey('Marca.id'))
    locatario_id = db.Column(db.Integer, db.ForeignKey('Usuario.id'))
    ativo = db.Column(db.Boolean, default=True)

    marca = db.relationship('Marca', backref='database')
    locatario = db.relationship('Usuario', backref='database')
    imagem = db.relationship('ImagemProduto')
   

class Marca(UserMixin, db.Model):
    __tablename__ = "Marca"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    logo = db.Column(db.Text)
    descricao = db.Column(db.Text)

class ImagemProduto(db.Model):
    __tablename__ = "ImagemProduto"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    caminho = db.Column(db.Text, nullable=False)
