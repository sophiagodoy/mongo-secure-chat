from db import get_db
from encryption import verifyPassword
from classes import User

# Função responsável por cadastrar o usuário 
def signUp():
    db = get_db()

    while True:
        username = input("Digite o nome de usuario: ").strip()
        if not username:
            print("Campo vazio, digite novamente!")
            continue
        
        # Verifica se usuário já está no banco
        user = db.Users.find_one({"username": username}) 
        if user:
            print("Este usuario ja existe, digite novamente")
            continue

        while True:
            p1 = input("Digite sua senha: ").strip()
            if not p1:
                print("Campo vazio, digite novamente!")
                continue
            
            p2 = input("Confirme sua senha: ").strip()
            if p1 == p2:
                usuario = User(username, p1)  
                print("Cadastro concluído com sucesso!")             
                return
            else:
                print("As senhas são diferentes, digite novamente!")

# Função responsável por fazer o login do usuário 
def signIn():
    db = get_db()

    while True:
        username = input("Digite seu nome de usuario: ")
        password = input("Digite sua senha: ")
        
        # Verifica se o usuário existe no banco
        user = db.Users.find_one({"username": username})
        if user:
            correctPassword = verifyPassword(password, user["password"])
        
        if not user or not correctPassword:  # se não achou o usuário ou senha errada
            print("Usuário ou senha incorretos.")
            num = int(input("Digite 1 para se cadastrar e 2 para tentar novamente: "))
            if num == 1:
                signUp()
                return
            elif num == 2:
                continue
            else:
                print("Opção inválida!")
                return
        else:
            print("\nUsuário logado com sucesso!")
            return user