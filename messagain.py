from db import get_db
from encryption import encryptMessage, decryptMessage
from classes import Message
import base64

# Função para enviar mensagem para outro usuário 
def sendMessage(sender):
    db = get_db()

    # Pede o destinatário
    receiver = input("Digite o @usuario do destinatário: ").strip()

    # Verifica se o campo está vazio
    if not receiver: 
        print("Você deve informar um destinatário válido.")
        return
    
    if receiver == sender:
        print("Você não pode enviar mensagem para si mesmo.")
        return

    # Confere se destinatário existe no banco de dados 
    user_dest = db.Users.find_one({"username": receiver})

    if not user_dest:
        print("Destinatário não encontrado.")
        return

    # Digita mensagem
    message = input("Digite sua mensagem: ").strip()

    if not message or not message.strip():
        print("Mensagem inválida: não pode ser vazia ou só espaços.")
        return

    if len(message) > 50:
        print("A mensagem deve ter no máximo 50 caracteres.")
        return

    # Pede chave secreta usada só para criptografar 
    secret_key = input("Digite a chave secreta para criptografar a mensagem: ").strip()
    
    if not secret_key:
        print("A chave secreta não pode ser vazia.")
        return

    # Criptografa a mensagem
    messageC = encryptMessage(message, secret_key)
    
    # Salva no banco
    mensagem = Message(sender, receiver, messageC)

    print("Mensagem criptografada e enviada com sucesso para", receiver)
    return

# Função para ler as mensagens recebidas e descriptografá-las        
def readMessages(username):
    db = get_db()

    while True:
        
        # Bucas as mensagens que estão com o status "nova", e pega a mais recente primeiro
        messages = list(db.Messages.find({"receiver": username, "status": "nova"}).sort("timestamp", -1))
        
        if not messages:
            print("\nVocê não tem mensagens novas no momento.")
            return

        print(f"\nVocê tem {len(messages)} mensagem(ns) nova(s):")
        
        # Mostra as mensagens numeradas pro usuário 
        for i, msg in enumerate(messages, 1):
            ts = msg.get("timestamp")
            when = ts.strftime("%d/%m/%Y %H:%M:%S") if ts else "sem data"
            print(f"[{i}] De: {msg['sender']} - {when}")

        # Escolhe a mensagem que deseja abrir
        choice = input("\nNúmero da mensagem para abrir (ou ENTER para voltar ao menu): ").strip()
        
        if not choice:
            return
        
        if not choice.isdigit():
            print("Entrada inválida! Digite apenas o número da mensagem.")
            continue

        idx = int(choice)
        if idx < 1 or idx > len(messages):
            print("Número inválido! Digite apenas o número da mensagem.")
            continue
        
        # Pego o documento escolhido pelo índice da lista
        selected = messages[idx - 1]

        # Pede a chave e tenta descriptografar
        secret = input("Digite a chave secreta: ").strip()

        if not secret:
            print("A chave secreta não pode ser vazia.")
            continue

        # Decodifica o conteúdo salvo no banco (tira do Base64 -> bytes criptografados)
        try:
            encrypted_bytes = base64.b64decode(selected["content"])
        except Exception:
            print("Formato inválido da mensagem (Base64).")
            continue

        # Tenta descriptografar a mensagem com a chave
        try:        
            text = decryptMessage(encrypted_bytes, secret)
            
            if text == None:
                print("Chave incorreta! ")
                continue

            print("\nMensagem descriptografada com sucesso:")
            print(text)

            # Marca a mensagem como “lida”
            db.Messages.update_one({"_id": selected["_id"]}, {"$set": {"status": "lida"}})
            print(f"Mensagem de {selected['sender']} marcada como lida.\n")
        except Exception:
            print("Não foi possível abrir a mensagem.")