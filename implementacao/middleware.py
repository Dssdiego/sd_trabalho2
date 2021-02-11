import zmq
import time
import random

print('Middleware ligado!')

# Lista de dispositivos
dispositivos = []

# Criação de contexto do ZeroMQ
context = zmq.Context()

# Socket para o envio das mensagens (clientes ou dispositivos)
pub = context.socket(zmq.PUB)
pub.bind("tcp://*:5555")

# Socket para resposta dos requests vindos dos dispositivos
repDisp = context.socket(zmq.REP)
repDisp.bind("tcp://*:6666")

# Socket para resposta dos requests vindos dos clientes
repClient = context.socket(zmq.REP)
repClient.bind("tcp://*:7777")

################ 
#   Clientes   #
################ 

def enviaMensagemCliente(msg):
    pub.send_string("client;" + str(msg))

def trataMensagemCliente(msg):
    mensagem = msg.split(';')
    header = mensagem[0]

    if header == "listaDisp":
        enviaMensagemCliente('Lista de Dispositivos: ' + str(dispositivos))

    if header == "ligaDisp":
        enviaMensagemDispositivo('ligaDisp;' + random.choice(dispositivos))

    if header == "desligaDisp":
        enviaMensagemDispositivo('desligaDisp;' + random.choice(dispositivos))

def recebeMensagemClientes():
    msg = repClient.recv_string()   # Recebe mensagem do dispositivo
    trataMensagemCliente(msg)       # Trata a mensagem
    repClient.send_string("ok")     # Envia a resposta de ok

################## 
#  Dispositivos  #
################## 

def registraDispositivo(dispId):
    if dispId not in dispositivos:
        dispositivos.append(dispId)

def enviaMensagemDispositivo(msg):
    pub.send_string("disp;" + str(msg))

def trataMensagemDispositivo(msg):
    mensagem = msg.split(';')
    header = mensagem[0]
    conteudo = mensagem[1]

    if header == "registra":
        registraDispositivo(conteudo)

    if header == "status":
        enviaMensagemCliente(conteudo)

    # if header == "getStatus":
    #     enviaMensagemCliente(conteudo)

def recebeMensagemDispositivo():
    msg = repDisp.recv_string()   # Recebe mensagem do dispositivo
    trataMensagemDispositivo(msg) # Trata a mensagem
    repDisp.send_string("ok")     # Envia a resposta de ok
    # print(msg)
    # print('dispositivos registrados: ' + str(dispositivos))
    # print("Received request: %s" % message)

############ 
#  Poller  #
############ 

# Gerência dos múltiplos sockets sem bloqueio
poller = zmq.Poller()
poller.register(repDisp, zmq.POLLIN)
poller.register(repClient, zmq.POLLIN)

# Loop para executar a comunicação
while True:
    socks = dict(poller.poll(1000))

    # Recebe as mensagens dos dispositivos
    if socks.get(repDisp) == zmq.POLLIN:
        recebeMensagemDispositivo()

    # Recebe as mensagens dos clientes
    if socks.get(repClient) == zmq.POLLIN:
        recebeMensagemClientes()

    # Pequeno atraso para melhor visualização dos logs
    time.sleep(0.4)