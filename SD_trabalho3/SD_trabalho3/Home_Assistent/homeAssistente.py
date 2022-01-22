
import grpc
import time
import atuador_pb2_grpc as pb2_grpc
import atuador_pb2 as pb2
import socket

localIP = "127.0.0.1"
localPort  = 20001
bufferSize = 1024
print("UDP server up and listening")
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
message = bytesAddressPair[0]
address = bytesAddressPair[1]


clientMsg = "Message from Client:{}".format(message)
clientIP  = "Client IP Address:{}".format(address)

print('Home Assistente Ligado');

channelAR = grpc.insecure_channel('localhost:50051')
Arcondicionado = pb2_grpc.atuadorServiceStub(channelAR)

chanelLuz = grpc.insecure_channel('localhost:50052')
lampada = pb2_grpc.atuadorServiceStub(chanelLuz)

channelAlarme = grpc.insecure_channel('localhost:50053')
alarme = pb2_grpc.atuadorServiceStub(channelAlarme)

while True:
    #chegada de dados de sensor:
    codigo = 1000
    valor = 30
    hora = ""


    #====================================================
    print("leitura seensor: ",codigo," ",valor," ",hora)

    if codigo == 1000:
        if valor >= 25:
            comando = pb2.command(info = 1)
            resp = Arcondicionado.sendInfo(comando)
        elif valor <= 17:
            comando = pb2.command(info = 0)
            resp = Arcondicionado.sendInfo(comando) 
    
    if codigo == 2000:
        if valor <= 40:
            comando = pb2.command(info = 1)
            resp = lampada.sendInfo(comando)
        else:
            comando = pb2.command(info = 0)
            resp = lampada.sendInfo(comando) 

    if codigo == 3000:
        if valor == 1:
            comando = pb2.command(info = 1)
            resp = alarme.sendInfo(comando)
        else:
            comando = pb2.command(info = 0)
            resp = alarme.sendInfo(comando)

    msgFromServer = resp
    bytesToSend = str.encode(msgFromServer)
    UDPServerSocket.sendto(bytesToSend, address)