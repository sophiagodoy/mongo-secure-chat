from pymongo import MongoClient

# Função com a lógica de conexão do banco 
def get_db():
    MONGO_URI = "mongodb+srv://SecureChat:SecureChat12345@securechatcluster.alxow7p.mongodb.net/?retryWrites=true&w=majority&appName=SecureChatCluster"
    client = MongoClient(MONGO_URI) # Cria a conexão com as cluster do banco 
    return client["Chat"] # Escolhemos qual banco desejamos usar