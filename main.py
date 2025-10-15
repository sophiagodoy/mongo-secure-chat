from account import (signIn, signUp)
from messagain import sendMessage, readMessages

# Menu inicial do programa 
def menuInicial():
    print("\nBem-vindo ao Chat Seguro com Python e MongoDB!")
    while True:
        print("===== MENU INICIAL =====")
        print("[1] ENTRAR")
        print("[2] CADASTRAR-SE")
        print("[0] SAIR")
        menu = int(input("Escolha: "))

        if menu == 1:
            userIn = signIn()
            if userIn:
                menuPrincipal(userIn)
        elif menu == 2:
            signUp()
        elif menu == 0:
            print("Saindo do chat...")
            break
        else:
            print("Opção inválida, tente novamente!")

# Menu principal do programa 
def menuPrincipal(user):
    while True:
        print("\n===== MENU DO CHAT =====")
        print("[1] Enviar mensagem")
        print("[2] Ler minhas mensagens")
        print("[0] Sair")
        escolha = input("Escolha: ")
        
        if escolha == "1":
            sendMessage(user["username"])
        elif escolha == "2":
            readMessages(user["username"])
        elif escolha == "0":
            print("Saindo do chat...")
            break
        else:
            print("Opção inválida, tente novamente.")


# Função principal do programa         
def main():
    menuInicial()

# Executa apenas se rodar direto este arquivo
if __name__ == "__main__":
    main()