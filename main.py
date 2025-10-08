from db import get_db
import bcrypt #Criptografia apenas para senhas (digitar no terminal: "python -m pip install bcrypt" para conseguir usar)
from cryptography.fernet import Fernet #Criptografia para mensagens
from bson.binary import Binary
import hashlib #Gerar chaves seguras usando a chave do usuario
import base64
from datetime import datetime

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

    def __init__(self, sender, receiver, messageContent: bytes):
        self._sender = sender
        self._receiver = receiver
        self.messageContent = base64.b64encode(messageContent).decode()
        self._status = "nova"
        self._timestamp = datetime.now()   
        self._saveNewMessage()

    def _saveNewMessage(self):
        self.db.Messages.insert_one({
            "sender": self._sender,
            "receiver": self._receiver,
            "content": self.messageContent,
            "status": self._status,
            "timestamp": self._timestamp
        })

# Método que criptografa o conteúdo da mensagem 
def encryptMessage(messageContent, key):
    fernet_key = generate_fernet_key(key)
    fernet = Fernet(fernet_key)
    return fernet.encrypt(messageContent.encode()) 

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
    messageC = encryptMessage(message, secret_key)
    print(messageC)
    # Salva no banco
    mensagem = Message(sender, receiver, messageC)

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
        if user:
            correctPassword = verify_password(password, user["password"])
        
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
            return
        
        
def readMessages(username):
    db = get_db()

    # pega só mensagens NOVAS desse usuário, mais recentes primeiro
    messages = list(
        db.Messages.find({"receiver": username, "status": "nova"}).sort("timestamp", -1)
    )

    if not messages:
        print("\nVocê não tem mensagens novas.")
        return

    print(f"\nVocê tem {len(messages)} mensagem(ns) nova(s):")
    for i, msg in enumerate(messages, 1):
        ts = msg.get("timestamp")
        when = ts.strftime("%d/%m/%Y %H:%M:%S") if ts else "sem data"
        print(f"[{i}] De: {msg['sender']} - {when}")

    # escolhe uma pra abrir
    choice = input("\nNúmero da mensagem para abrir: ").strip()
    if not choice.isdigit():
        print("Entrada inválida.")
        return

    idx = int(choice)
    if idx < 1 or idx > len(messages):
        print("Número inválido.")
        return
    
    # Pego o documento escolhido
    selected = messages[idx - 1]

    # pede a chave e tenta descriptografar
    secret = input("Digite a chave secreta: ").strip()
    if not secret:
        print("A chave secreta não pode ser vazia.")
        return

    # 1) tira do Base64 -> bytes criptografados
    try:
        encrypted_bytes = base64.b64decode(selected["content"])
    except Exception:
        print("Formato inválido da mensagem (Base64).")
        return

    # 2) tenta descriptografar com a chave
    try:
        f = Fernet(generate_fernet_key(secret))
        text = f.decrypt(encrypted_bytes).decode()
        print("\n✅ Mensagem descriptografada com sucesso:")
        print(text)

        # 3) marca como lida
        db.Messages.update_one({"_id": selected["_id"]}, {"$set": {"status": "lida"}})
        print("✅ Mensagem marcada como lida.")
    except Exception:
        print("❌ Chave incorreta! Não foi possível abrir a mensagem.")


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