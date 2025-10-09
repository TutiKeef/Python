from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

#CONFIGURAÇÃO DO BANCO DE DADOS______________________________
db = create_engine("sqlite:///pythonalchemy/meubanco.db")
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()
#MODELO AQUI NO MEIO_______________________________________________

#as tabelas

#nova classe_________________________________________________________
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement = True)
    nome = Column ("nome", String)
    email = Column ("email", String)
    senha = Column ("senha", String)
    ativo = Column ("ativo", Boolean)

#getters e setters
    def __init__(self, nome, email, senha, ativo = True):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo

#nova classe_________________________________________________________
class Livro(Base):
    __tablename__ = "livros"

    id = Column("id", Integer, primary_key=True, autoincrement = True)
    titulo = Column("titulo", String)
    qtd_paginas = Column("qtd_paginas",Integer)
    dono = Column("dono",ForeignKey("usuarios.id"))

#getters e setters
    def __init__(self, titulo, qtd_paginas, dono):
        self.titulo = titulo
        self.qtd_paginas = qtd_paginas
        self.dono = dono




#MODELOS AQUI NO MEIO________________________________________________
Base.metadata.create_all(bind=db)

#FUNÇÕES CRUD (CREATE, READ,UPDATE, DELETE)_____________________________________________

#EX: criar_usuario("João", "joao@email.com", "1234")
def criar_usuario(nome, email, senha, ativo = True):
    usuario = Usuario(nome,email,senha,ativo)
    session.add(usuario)
    session.commit()
    print(f"Usuário '{nome}' criado com sucesso")

#EX: listar_usuarios()
def listar_usuarios():
    usuarios = session.query(Usuario).all()
    for u in usuarios:
        print(f"{u.id} | {u.nome} | {u.email} | Ativo: {u.ativo}")

    return usuarios

#EX: buscar_usuario_por_id(1)
def buscar_usuario_por_id(user_id):
    usuario = session.query(Usuario).filter_by(id=user_id).first()
    if usuario:
        print(f"{usuario.id} | {usuario.nome} | {usuario.email}")
    else:
        print("Usuário não encontrado!")
    return usuario

#EX: atualizar_usuario(1, nome="João da Silva", ativo=False)
def atualizar_usuario(user_id, nome=None, email=None, senha=None, ativo=None):
    usuario = buscar_usuario_por_id(user_id)
    if usuario:
        if nome:
            usuario.nome = nome
        if email:
            usuario.email = email
        if senha:
            usuario.senha = senha
        if ativo is not None:
            usuario.ativo=ativo

        session.commit()

#EX: deletar_usuario(2)
def deletar_usuario(user_id):
    usuario = buscar_usuario_por_id(user_id)
    if usuario:
        session.delete(usuario)
        session.commit()
        print(f"Usuário {user_id} deletado com sucesso")

