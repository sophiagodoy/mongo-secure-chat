from db import get_db
import bcrypt #Criptografia apenas para senhas (digitar no terminal: "python -m pip install bcrypt" para conseguir usar)
from cryptography.fernet import Fernet #Criptografia para mensagens
import hashlib #Gerar chaves seguras usando a chave do usuario
import base64

# Definindo a classe que representa o usuário 
class User:
    db = get_db()
    
    # Salva no banco de dados 
    def __saveUserDB(self):
        try:
            self.db.Users.insert_one ({
                "username": self.__username,
                "password": self.__password
            })
            print("Usuario salvo.")
        except Exception as e:
            print("Não foi possivel salvar o usuario.", e)

    # Construtor da classe User (cria usuário novo)
    def __init__(self, username, password):
         self.__username = username
         self.__password = hash_password(password) # Salva a senha já criptografada
         self.__saveUserDB()

# Definindo a classe que representa a mensagem 
class Message:
    db = get_db()

    def __init__(self, sender, receiver, messageContent):
        self.__sender = sender
        self.__receiver = receiver
        self.___messageContent = messageContent
        self.__status = "Nova"
        self.__saveNewMessage()

    def __saveNewMessage(self):
        self.db.Messages.insert_one({
            "Sender": self.__sender,
            "Receiver": self.__receiver,
            "Content": self.___messageContent,
            "Status": self.__status
        })

# Método que criptografa o conteúdo da mensagem 
def encryptMessage(messageContent, key):
    fernet_key = generate_fernet_key(key)
    fernet = Fernet(fernet_key)
    encrypt_message = fernet.encrypt(messageContent.encode())
    return encrypt_message

# Descriptografa uma mensagem, usando a chave que o usuário digitar
def decryptMessage(message, keyTest): # parametro message é apenas o conteudo criptografado da mensagem, keyTest é a chave que quem vai ler tentou usar
    fernet_teste = Fernet(generate_fernet_key(keyTest))
    try:
        decrypt_message = fernet_teste.decrypt(message).decode()
        print("\nMensagem descriptografada com sucesso:", decrypt_message) #print para teste, caso funcione implementar a leitura depois
    except Exception:
        print("Chave incorreta! Tente novamente.")

# Criptografa a senha do usuário antes de salvar
def hash_password(password):
        salt = bcrypt.gensalt()  # gera um salt seguro
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed.decode()  # salva como string no banco

# Verifica se a senha digitada bate com a que está no banco
def verify_password(passwordInput, otherPassword):
        return bcrypt.checkpw(passwordInput.encode(), otherPassword.encode())

# Gera uma chave Fernet válida a partir da senha simples digitada
def generate_fernet_key(user_key: str) -> bytes: #gera uma chave segura usando a digitada pelo usuario
    hash_key = hashlib.sha256(user_key.encode()).digest()
    return base64.urlsafe_b64encode(hash_key)

# Menu inicial do programa 
def menuInicial():
    print("\n===== MENU INICIAL =====")
    print("[1] ENTRAR")
    print("[2] CADASTRAR-SE")
    print("QUALQUER TECLA PARA SAIR")
    menu = int(input("Escolha: "))
    return menu

# Menu principal do programa 
def menuPrincipal():
    print("\n===== MENU DO CHAT =====")
    print("[1] Enviar mensagem")
    print("[2] Ler minhas mensagens")
    print("[0] Sair")
    escolha = input("Escolha: ")
    return escolha

# Função para enviar mensagem para outro usuário 
def sendMessage(sender):
    db = get_db()

    # Pede o destinatário
    receiver = input("Digite o @usuario do destinatário: ").strip()
    if not receiver: # Verifica se o campo está vazio
        print("Você deve informar um destinatário válido.")
        return
    if receiver == sender:
        print("Você não pode enviar mensagem para si mesmo.")
        return

    # Confere se destinatário existe 
    user_dest = db.Users.find_one({"username": receiver})
    if not user_dest:
        print("Destinatário não encontrado.")
        return

    # Digita mensagem
    message = input("Digite sua mensagem (mínimo 50 caracteres): ").strip()
    if not message or not message.strip():
        print("Mensagem inválida: não pode ser vazia ou só espaços.")
        return
    if len(message) < 50:
        print("A mensagem deve ter pelo menos 50 caracteres.")
        return

    # Pede chave secreta usada só para criptografar 
    secret_key = input("Digite a chave secreta para criptografar a mensagem: ").strip()
    if not secret_key:
        print("A chave secreta não pode ser vazia.")
        return

    # Criptografa a mensagem
    message = encryptMessage(message, secret_key)

    # Salva no banco
    mensagem = Message(sender, receiver, message)

    print("Mensagem criptografada e enviada com sucesso para", receiver)
    return

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
        
        if not user:  # se não achou o usuário
            print("Usuário não encontrado.")
            num = int(input("Digite 1 para se cadastrar e 2 para tentar novamente: "))
            if num == 1:
                signUp()
                return
            elif num == 2:
                continue
            else:
                print("Opção inválida!")
                return

        # Se o usuário existe, vai verificar a senha
        correctPassword = verify_password(password, user["password"])
        
        if not correctPassword:  # senha incorreta
            print("Senha incorreta!")
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
            
            while True:
                print("\n===== MENU DO CHAT =====")
                print("[1] Enviar mensagem")
                print("[2] Ler minhas mensagens")
                print("[0] Sair")
                escolha = input("Escolha: ")

                if escolha == "1":
                    sendMessage(user["username"])
                elif escolha == "2":
                    print("Aqui chamaria a função de ler mensagens...") # ARTHUR - CHAMAR FUNÇÃO DE LER MENSAGENS AQUI 
                elif escolha == "0":
                    print("Saindo do chat...")
                    break
                else:
                    print("Opção inválida, tente novamente.")
            return

# Função principal do programa         
def main():
    menu = menuInicial()

    while menu >= 1 and menu <= 2:
        if menu == 1:
            signIn()
        else:
            signUp()
        menu = menuInicial()

# Executa apenas se rodar direto este arquivo
if __name__ == "__main__":
    main()