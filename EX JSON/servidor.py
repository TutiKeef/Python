import socket
import threading
import json
import os

USUARIOS_DB = "usuarios.json"
MENSAGENS_DB = "mensagens.json"

#======================= Função auxiliares =======================
def carregar_json(arquivo):
    if not os.path.exists(arquivo):
        with open(arquivo,"w", encoding="utf-8") as f:
            json.dump([], f)
    with open(arquivo,"r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def salvar_json(arquivo,dados):
    with open(arquivo,"w", encoding="utf-8") as f:
        json.dump(dados,f, indent=4, ensure_ascii=False)

#======================= Cadastro e login =======================
def cadastrar_usuario(nome, email):
    usuarios = carregar_json(USUARIOS_DB)
    for u in usuarios:
        if u ["nome"] == nome:
            return "Usuário já existe"

    nova = {"nome": nome, "email": email}
    usuarios.append(nova)
    salvar_json(USUARIOS_DB, usuarios)
    return f"Usuário {nome} criado com sucesso"

def verificar_usuario(nome):
    usuarios = carregar_json(USUARIOS_DB)
    for u in usuarios:
        if u["nome"] == nome:
            return True
    return False

#=======================Envio e salvamento de mensagens=======================
def salvar_mensagem(remetente,texto):
    mensagens = carregar_json(MENSAGENS_DB)
    mensagens.append({"de": remetente, "mensagem": texto})
    salvar_json(MENSAGENS_DB, mensagens)


#=======================Servidor TCP=======================
HOST = "127.0.0.1"
PORT = 5555

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()

clientes = []
nomes = {}

print(f"Servidor rodando em {HOST}:{PORT}")

def broadcast(mensagem, remetente=None):
    """ENvia mensagem para todos os clientes conectados (Broadcast)"""
    for cliente in clientes:
        try:
            if remetente:
                cliente.send(f"{remetente}: {mensagem}".encode("utf-8"))
            else:
                cliente.send(mensagem.encode("utf-8"))
        except:
            cliente.close()
            clientes.remove(cliente)

def handle_cliente(conn, addr):
    print(f"Nova conexão com {addr}")
    conn.send("Digite seu nome".encode("utf-8"))
    nome = conn.recv(1024).decode("utf-8").strip()

    if not verificar_usuario(nome):
            conn.send("Usuário não encontrado. Digite o email para cadastro".encode("utf-8"))
            email = conn.recv(1024).decode("utf-8").strip()
            resposta = cadastrar_usuario(nome, email)
            conn.send(f"{resposta}".encode("utf-8"))

    else:
        conn.send("Login realizado com sucesso\n".encode("utf-8"))

    nomes[conn] = nome
    clientes.append(conn)
    broadcast(f"{nome} entrou no chat")


    while True:
        try:
            msg = conn.recv(1024).decode("utf-8").strip()
            if not msg:
                break
            salvar_mensagem(nome, msg)
            broadcast(msg, remetente=nome)
        except:
            break

    print(f"{nome} desconectou")
    clientes.remove(conn)
    broadcast(f"{nome} saiu do chat")
    conn.close()



#Loop principal para aceitar conexões
while True:
    conn, addr = servidor.accept()
    thread = threading.Thread(target=handle_cliente, args=(conn, addr))
    thread.start()
