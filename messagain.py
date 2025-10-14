from db import get_db
from encryption import encryptMessage, decryptMessage
from classes import Message
import base64
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
    message = input("Digite sua mensagem: ").strip()
    if not message or not message.strip():
        print("Mensagem inválida: não pode ser vazia ou só espaços.")
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
        
def readMessages(username):
    db = get_db()

    while True:
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
        choice = input("\nNúmero da mensagem para abrir (ou ENTER para voltar ao menu): ").strip()
        if not choice:
            return
        if not choice.isdigit():
            print("Entrada inválida.")
            continue

        idx = int(choice)
        if idx < 1 or idx > len(messages):
            print("Número inválido.")
            continue
        
        # Pego o documento escolhido
        selected = messages[idx - 1]

        # pede a chave e tenta descriptografar
        secret = input("Digite a chave secreta: ").strip()
        if not secret:
            print("A chave secreta não pode ser vazia.")
            continue

        # 1) tira do Base64 -> bytes criptografados
        try:
            encrypted_bytes = base64.b64decode(selected["content"])
        except Exception:
            print("Formato inválido da mensagem (Base64).")
            continue

        # 2) tenta descriptografar com a chave
        try:        
            text = decryptMessage(encrypted_bytes, secret)
            if text == None:
                print("Chave incorreta! ")
                continue
            print("\nMensagem descriptografada com sucesso:")
            print(text)

            # 3) marca como lida
            db.Messages.update_one({"_id": selected["_id"]}, {"$set": {"status": "lida"}})
            print("Mensagem marcada como lida.")
        except Exception:
            print("Não foi possível abrir a mensagem.")