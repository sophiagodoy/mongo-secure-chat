import bcrypt # Criptografia apenas para senhas (digitar no terminal: "python -m pip install bcrypt" para conseguir usar)
from cryptography.fernet import Fernet # Criptografia para mensagens
from bson.binary import Binary
import hashlib # Gerar chaves seguras usando a chave do usuario
import base64

# Método que criptografa o conteúdo da mensagem 
def encryptMessage(messageContent, key):
    fernet_key = generateFernetKey(key)
    fernet = Fernet(fernet_key)
    return fernet.encrypt(messageContent.encode()) 

# Descriptografa uma mensagem, usando a chave que o usuário digitar
def decryptMessage(message, keyTest): # Parametro message é apenas o conteudo criptografado da mensagem, keyTest é a chave que quem vai ler tentou usar
    fernet_teste = Fernet(generateFernetKey(keyTest))
    try:
        decrypt_message = fernet_teste.decrypt(message).decode()
        return decrypt_message
    except Exception:
        print("Chave incorreta! Tente novamente.")

# Criptografa a senha do usuário antes de salvar
def hashPassword(password):
        salt = bcrypt.gensalt()  # Gera um salt seguro
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed.decode()  # Salva como string no banco

# Verifica se a senha digitada esta correta
def verifyPassword(passwordInput, otherPassword):
        return bcrypt.checkpw(passwordInput.encode(), otherPassword.encode())

def generateFernetKey(user_key: str) -> bytes: # Gera uma chave segura usando a digitada pelo usuario
    hash_key = hashlib.sha256(user_key.encode()).digest()
    return base64.urlsafe_b64encode(hash_key)