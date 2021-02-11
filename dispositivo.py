import zmq
import time
import random

# Criação de contexto do ZeroMQ
context = zmq.Context()

# Id único do dispositivo
uuid = random.randrange(0,9999)
print('dispositivo ' + str(uuid))

# Definições de status
status = 'DESLIGADO'

# Socket para envio de mensagens ao middleware
req = context.socket(zmq.REQ)
req.connect("tcp://localhost:6666")

# Socket para recebimento das mensagens do middleware
sub = context.socket(zmq.SUB)
sub.connect("tcp://localhost:5555")
sub.setsockopt_string(zmq.SUBSCRIBE, "disp")

def enviaMensagemMiddleware(comando):
    req.send_string(str(comando) + ";" + str(uuid))
    msg = req.recv()
    # print(msg)

def registraMiddleware():
    enviaMensagemMiddleware("registra")

def desligaDispositivo(dispId):
    if str(uuid) == str(dispId):
        print('Okay middleware, recebi sua mensagem... Vou agir!')
        status = 'DESLIGADO'
        print('Desliguei :(')
        enviaMensagemMiddleware('status;Dispositivo ' + str(uuid) + ' ' + str(status))

def ligaDispositivo(dispId):
    if str(uuid) == str(dispId):
        print('Okay middleware, recebi sua mensagem... Vou agir!')
        status = 'LIGADO'
        print('Liguei :)')
        enviaMensagemMiddleware('status;Dispositivo ' + str(uuid) + ' ' + str(status))

def trataMensagemMiddleware(msg):
    mensagem = msg.split(';')
    header = mensagem[1]
    dispId = mensagem[2]

    if header == "ligaDisp":
        ligaDispositivo(dispId)

    if header == "desligaDisp":
        desligaDispositivo(dispId)

    # print(mensagem)

def recebeMensagemMiddleware():
    msg = sub.recv_string()
    trataMensagemMiddleware(msg)
    # print('veio do middleware: ' + msg)

# Loop para executar a comunicação
while True:
    # Registra no middleware
    registraMiddleware()

    # Recebe as mensagens do middleware
    recebeMensagemMiddleware()