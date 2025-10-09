import tkinter as tk
from tkinter import messagebox
from meubanco import criar_usuario, listar_usuarios

def cadastrar_usuario():
    nome = entry_nome.get()
    email = entry_email.get()
    senha = entry_senha.get()

    if nome and email and senha:
        criar_usuario(nome, email, senha)
        messagebox.showinfo("Sucesso", f"Usuário '{nome}' criado com sucesso!")
        entry_nome.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_senha.delete(0, tk.END)
    else:
        messagebox.showwarning("Aviso", "Preencha todos os campos!")

def mostrar_usuarios():
    lista = listar_usuarios()
    texto.delete("1.0", tk.END)
    if lista:
        for u in lista:
            texto.insert(tk.END, f"{u.id} | {u.nome} | {u.email} | Ativo: {u.ativo}\n")
    else:
        texto.insert(tk.END, "Nenhum usuário encontrado.")

# ------------------ GUI ------------------
janela = tk.Tk()
janela.title("Gerenciador de Usuários")
janela.geometry("500x400")

tk.Label(janela, text="Nome:").pack()
entry_nome = tk.Entry(janela)
entry_nome.pack()

tk.Label(janela, text="Email:").pack()
entry_email = tk.Entry(janela)
entry_email.pack()

tk.Label(janela, text="Senha:").pack()
entry_senha = tk.Entry(janela, show="*")
entry_senha.pack()

tk.Button(janela, text="Cadastrar Usuário", command=cadastrar_usuario).pack(pady=5)
tk.Button(janela, text="Listar Usuários", command=mostrar_usuarios).pack(pady=5)

texto = tk.Text(janela, height=10, width=60)
texto.pack()

janela.mainloop()
