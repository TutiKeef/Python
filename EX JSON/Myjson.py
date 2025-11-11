import json
import os


#Onde vai armazenar os dados
ARQUIVO = "Usuarios.json"

#Função para carregar dados existentes
def carregar_dados():
    # Se o arquivo não existir, cria um JSON vazio (lista)
    if not os.path.exists(ARQUIVO):
        with open(ARQUIVO, "w", encoding="utf-8") as f:
            json.dump([], f)

    # Agora tenta carregar com segurança
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        try:
            dados = json.load(f)
        except json.JSONDecodeError:
            # Se o arquivo estiver vazio ou corrompido, reinicia
            dados = []
    return dados


#Função parar salvar dados no arquivo
def salvar_dados(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados,f, indent=4, ensure_ascii=False)

#Função principal
def criar_usuario():
    nome = input("Nome: ")
    idade = int(input("Idade: "))
    email = input("Email: ")

    usuario = {
        "nome": nome,
        "idade": idade,
        "email": email
    }

    #Carrega db existente
    dados = carregar_dados()

    #Adiciona o novo registro
    dados.append(usuario)

    #Salva de volta no arquivo
    salvar_dados(dados)

    print(f"\nUsuário {nome} salvo com sucesso!")

    #Função para listar todos os usuários cadastrados
def listar_usuarios():
    dados = carregar_dados()
    if not dados:
        print("Nenhum usuário cadastrado ainda")
        return
    print("\n Usuários cadastrados: ")
    for i, user in enumerate(dados, start=1):
        print(f"{i}. {user['nome']} - {user['idade']} ({user['email']})")

#LOOP PRINCIPAL
while True:
    print("\n== MENU ==")
    print("1 - Cadastrar usuário")
    print("2 - Listar usuarios")
    print("3 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        criar_usuario()
    elif opcao == "2":
        listar_usuarios()
    elif opcao == "3":
        print("Saindo do sistema")
        break
    elif opcao == "4":

        print("Entra no chat")
    else:
        print("Opção inválida, tente novamente")