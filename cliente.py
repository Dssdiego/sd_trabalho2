import zmq
import time
import random
import sys
import os

# Define o comando para limpar a tela
clear = lambda: os.system('clear')

# Criação de contexto do ZeroMQ
context = zmq.Context()

# Id único do cliente
uuid = random.randrange(0,9999)
print('cliente ' + str(uuid))

# Socket para envio de mensagens ao middleware
req = context.socket(zmq.REQ)
req.connect("tcp://localhost:7777")

# Socket para recebimento das mensagens do middleware
sub = context.socket(zmq.SUB)
sub.connect("tcp://localhost:5555")
sub.setsockopt_string(zmq.SUBSCRIBE, "client")

def enviaMensagemMiddleware(comando):
    req.send_string(str(comando) + ";" + str(uuid))
    msg = req.recv()

def trataMensagemMiddleware(msg):
    mensagem = msg.split(';')
    header = mensagem[0]
    conteudo = mensagem[1]
    print(conteudo)

def recebeMensagemMiddleware():
    msg = sub.recv_string()
    trataMensagemMiddleware(msg)

# Loop para executar a comunicação
while True:
    # Manda uma mensagem para verificar a lista de dispositivos conectados no middleware
    enviaMensagemMiddleware("listaDisp")

    # Manda uma mensagem para ligar algum dispositivo aleatório da rede
    enviaMensagemMiddleware("ligaDisp")

    # Manda uma mensagem para desligar algum dispositivo aleatório da rede
    enviaMensagemMiddleware("desligaDisp")

    # Recebe as mensagens do middleware
    recebeMensagemMiddleware()