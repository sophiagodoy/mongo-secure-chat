from db import get_db
import bcrypt #Criptografia apenas para senhas (digitar no terminal: "python -m pip install bcrypt" para conseguir usar)
from cryptography.fernet import Fernet #Criptografia para mensagens
import hashlib #Gerar chaves seguras usando a chave do usuario
import base64

class User:
    db = get_db()
    def __saveUserDB(self):
        try:
            self.db.Users.insert_one ({
                "username": self.__username,
                "password": self.__password
            })
            print("Usuario salvo.")
            signIn()
        except Exception as e:
            print("Não foi possivel salvar o usuario.", e)

    def __init__(self, username, password):
         self.__username = username
         self.__password = hash_password(password)
         self.__saveUserDB()

class Message:
    db = get_db()
    def __init__(self, messageContent):
        self.___messageContent = messageContent
        #Implementar os outros atributos

    def __encryptMessage(self, key):
        fernet_key = generate_fernet_key(key)
        fernet = Fernet(fernet_key)
        encrypt_message = fernet.encrypt(self.___messageContent.encode())
        #Adicionar mensagem criptografada no banco

def decryptMessage(message, keyTest): #parametro message é apenas o conteudo criptografado da mensagem, keyTest é a chave que quem vai ler tentou usar
    fernet_teste = Fernet(generate_fernet_key(keyTest))
    try:
        decrypt_message = fernet_teste.decrypt(message).decode()
        print("\nMensagem descriptografada com sucesso:", decrypt_message) #print para teste, caso funcione implementar a leitura depois
    except Exception:
        print("Chave incorreta! Tente novamente.")


def hash_password(password):
        salt = bcrypt.gensalt()  # gera um salt seguro
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed.decode()  # salva como string no banco

def verify_password(passwordInput, otherPassword):
        return bcrypt.checkpw(passwordInput.encode(), otherPassword.encode())

def generate_fernet_key(user_key: str) -> bytes: #gera uma chave segura usando a digitada pelo usuario
    hash_key = hashlib.sha256(user_key.encode()).digest()
    return base64.urlsafe_b64encode(hash_key)

def menuInicial():
    print("\n===== MENU INICIAL =====")
    print("[1] ENTRAR")
    print("[2] CADASTRAR-SE")
    print("QUALQUER TECLA PARA SAIR")
    menu = int(input("Escolha: "))
    return menu

def signUp():
    db = get_db()
    while True:
        username = input("Digite o nome de usuario: ").strip()
        if not username:
            print("Campo vazio, digite novamente!")
            continue
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
                return
            else:
                print("As senhas são diferentes, digite novamente!")

def signIn():
    db = get_db()
    while True:
        username = input("Digite seu nome de usuario: ")
        password = input("Digite sua senha: ")
        user = db.Users.find_one({"username": username})
        correctPassword = verify_password(password, user["password"])
        if not user or not correctPassword:
            print("Usuario ou senha incorretos")
            num = int(input("Digite 1 para se cadastrar e 2 para tentar novamente: "))
            if num == 1:
                signUp()
            elif num == 2:
                continue
            else:
                print("Opção invalida!")
                return
        else:
            
            print("Usuario logado")
            return
        
def main():
    menu = menuInicial()
    while menu >= 1 and menu <= 2:
        if menu == 1:
            signIn()
        else:
            signUp()
        menu = menuInicial()

if __name__ == "__main__":
    main()