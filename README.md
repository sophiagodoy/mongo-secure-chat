# 🔐 Chat Seguro com Python e MongoDB

## Sobre o Projeto
- Este projeto é um **chat seguro via terminal (CLI)** desenvolvido em **Python**, utilizando **MongoDB Atlas** como banco de dados.  
- As mensagens são **criptografadas com uma chave secreta**, garantindo que apenas quem a possui consiga ler o conteúdo.

## Tecnologias Utilizadas
- **Python**
- **MongoDB Atlas**
- **Cryptography / Fernet** 
  
Principais Funcionalidades
- Cadastro e login de usuários com senha criptografada
- Envio e recebimento de mensagens cifradas
- Validação de chave secreta para leitura de mensagens
- Alteração automática do status de mensagens de “nova” para “lida”

## Como Executar
2. Clone este repositório:
   ```sh
   git@github.com:sophiagodoy/mongo-secure-chat.git

2. Instale as dependências necessárias
   
4. Para executar o programa faça
   ```sh
   python main.py
