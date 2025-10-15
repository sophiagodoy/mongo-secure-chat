from db import get_db
from encryption import hashPassword
from datetime import datetime
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
         self.__password = hashPassword(password) # Salva a senha já criptografada
         self.__saveUserDB()

# Definindo a classe que representa a mensagem 
class Message:
    db = get_db()

    # Constrói o objeto de mensagem e salva automaticamente no banco de dados
    def __init__(self, sender, receiver, messageContent: bytes):
        self._sender = sender
        self._receiver = receiver
        self.messageContent = base64.b64encode(messageContent).decode()
        self._status = "nova"
        self._timestamp = datetime.now()   
        self._saveNewMessage()
    
    # Salva a mensagem no banco de dados 
    def _saveNewMessage(self):
        self.db.Messages.insert_one({
            "sender": self._sender,
            "receiver": self._receiver,
            "content": self.messageContent,
            "status": self._status,
            "timestamp": self._timestamp
        })