import grpc
import time
import atuador_pb2_grpc as pb2_grpc
import atuador_pb2 as pb2
import socket
import threading as th

localIP = "127.0.0.1"
commandPort  = 5000
responsePort = 5001
bufferSize = 1024
adminAddress = None

commandSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
responseSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)

commandSocket.bind((localIP, commandPort))
responseSocket.bind((localIP, responsePort))

print('Home Assistente Ligado')

#configuração de conexão com serviços de atuadores ============================================
channelAR = grpc.insecure_channel('localhost:50051')
Arcondicionado = pb2_grpc.atuadorServiceStub(channelAR)

chanelLuz = grpc.insecure_channel('localhost:50052')
lampada = pb2_grpc.atuadorServiceStub(chanelLuz)

channelAlarme = grpc.insecure_channel('localhost:50053')
alarme = pb2_grpc.atuadorServiceStub(channelAlarme)


def getConexionFromClient():
    print("Aguardando Conexão do cliente")
    bytesNewClient = responseSocket.recvfrom(bufferSize)
    messageClient = bytesNewClient[0]
    adminAddress = bytesNewClient[1]
    clientMsg = format(messageClient)
    clientIP  = format(adminAddress)
    print(clientIP," ",clientMsg)

def rootCommandoToAtuador(codigoRec, comandoRec):
    print("root Chamado!")
    if codigoRec == 1000:
        if comandoRec == 1 or comandoRec == 0:
            comando = pb2.command(info = comandoRec)
            resp = Arcondicionado.sendInfo(comando)
        else:
             resp = "Comando enviado invalido"

    elif codigoRec == 2000:
        if comandoRec == 1 or comandoRec == 0:
            comando = pb2.command(info = comandoRec)
            resp = lampada.sendInfo(comando)
        else:
             resp = "Comando enviado invalido"  
        
    elif codigoRec == 3000:
        if comandoRec == 1 or comandoRec == 0:
            comando = pb2.command(info = comandoRec)
            resp = alarme.sendInfo(comando)
        else:
             resp = "Comando enviado invalido"

    else:
        if(comandoRec == 0 or comandoRec == 1):
            resp = "O codigo enviado não coorresponde a nenhum atuador"  
    
    print(resp)
    
    global adminAddress
    if(adminAddress != None):
        msgFromServer = resp
        bytesToSend = str.encode(msgFromServer)
        responseSocket.sendto(bytesToSend, adminAddress)


def receiveCommandFromClient():
    print("Aguardando Comando do cliente")
    while True:
        bytesCommand = commandSocket.recvfrom(bufferSize)
        messageCommand = bytesCommand[0]
        addressSenderCommand = [1]
        clientMsg = format(messageCommand)
        clientIP  = format(addressSenderCommand)
        print(clientIP," ",clientMsg)


def receiveDataFromSensor():
    print("Aguardando dados do sensor")
    while True:
        #chegada de dados de sensor:
        time.sleep(99999)
        codigo = 1000;
        valor = 30
        hora = ""
        #====================================================
        print("leitura sensor: ",codigo," ",valor," ",hora)
               
        if codigo == 1000:
            if valor >= 25:
                rootCommandoToAtuador(codigoRec = codigo, comandoRec = 1)
            elif valor <= 17:
                rootCommandoToAtuador(codigoRec = codigo, comandoRec = 0)
     
        if codigo == 2000:
            if valor <= 40:
                rootCommandoToAtuador(codigoRec = codigo, comandoRec = 1)
            else:
                rootCommandoToAtuador(codigoRec = codigo, comandoRec = 0)
        
        if codigo == 3000:
            if valor == 1:
                rootCommandoToAtuador(codigoRec = codigo, comandoRec = 1)
            else:
                rootCommandoToAtuador(codigoRec = codigo, comandoRec = 1)


#=====================================================================================================
th.Thread(target = getConexionFromClient).start()
th.Thread(target = receiveCommandFromClient).start()
th.Thread(target = receiveDataFromSensor).start()

print("its are working")