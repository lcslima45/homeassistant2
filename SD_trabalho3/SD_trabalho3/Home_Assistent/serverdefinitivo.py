
import pika
import json
import grpc
import threading as th
import socket;
import atuador_pb2_grpc as pb2_grpc
import atuador_pb2 as pb2

host = "127.0.0.1"
port = 5000;

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen();

clients = []

#=========================Configuração de conexão com serviços de atuadores =================================
channelAR = grpc.insecure_channel('localhost:50051')
Arcondicionado = pb2_grpc.atuadorServiceStub(channelAR)

chanelLuz = grpc.insecure_channel('localhost:50052')
lampada = pb2_grpc.atuadorServiceStub(chanelLuz)

channelAlarme = grpc.insecure_channel('localhost:50053')
alarme = pb2_grpc.atuadorServiceStub(channelAlarme)


#==================================Roteamento de comandos para Atuadores=============================

def rootCommandoToAtuador(codigoRec, comandoRec):
    
    if codigoRec == 1000:
        if comandoRec == 1 or comandoRec == 0:
            comando = pb2.command(info = comandoRec)
            respAt = Arcondicionado.sendInfo(comando)
            cod = respAt.codigo
            nom = respAt.nome
            mess = respAt.mensagem
            resp = [cod, nom, mess]
            
        else:
             respAt = ["Comando enviado eh invalido"]

    elif codigoRec == 2000:
        if comandoRec == 1 or comandoRec == 0:
            comando = pb2.command(info = comandoRec)
            respAt =  lampada.sendInfo(comando)
            cod = respAt.codigo
            nom = respAt.nome
            mess = respAt.mensagem
            resp = [cod, nom, mess]
        else:
             resp = ["Comando enviado eh invalido"] 
        
    elif codigoRec == 3000:
        if comandoRec == 1 or comandoRec == 0:
            comando = pb2.command(info = comandoRec)
            respAt = alarme.sendInfo(comando)
            cod = respAt.codigo
            nom = respAt.nome
            mess = respAt.mensagem
            resp = [cod, nom, mess]
        else:
            resp = ["Comando enviado eh invalido"]

    else:
        resp = ["O codigo enviado não coorresponde a nenhum atuador"]
    
    mjson = json.dumps(resp)
    print("Resp:",mjson)
    messageToClient = mjson.encode('ascii')
    broadcast(messageToClient)


def sendSensorDataToAtuador(codigo, valorLido):
    if codigo == 1000:
        if valorLido >= 28:
            rootCommandoToAtuador(codigoRec=codigo, comandoRec=1)
        else:
            rootCommandoToAtuador(codigoRec=codigo, comandoRec=0)

    elif codigo == 2000:
        if valorLido <= 40:
            rootCommandoToAtuador(codigoRec=codigo, comandoRec=1)
        else:
            rootCommandoToAtuador(codigoRec=codigo, comandoRec=0)

    elif codigo == 3000:
        if valorLido == 1:
            rootCommandoToAtuador(codigoRec=codigo, comandoRec=1)
        else:
            rootCommandoToAtuador(codigoRec=codigo, comandoRec=0)


#=============================Servidor UDP para comunicação com cliente============================================    

def broadcast(message):
    for client_i in clients:
        client_i.send(message);


def handle(client):
    while True:
        try:
            message =  client.recv(1024);
            msg = message.decode('ascii')
            msg = json.loads(msg)
            code = int(msg[1])
            comm = int(msg[2])
            print("Req client: ", msg)
            rootCommandoToAtuador(codigoRec=code, comandoRec=comm)
           
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close() 
            break

def receiveClient():
    while True:
        client, address = server.accept()
        print(f"Conectado com endereço {str(address)}")
        client.send('conectado com sucesso'.encode('ascii'))
        clients.append(client)
        print("=============================================================")

        th.Thread(target = handle, args = (client, )).start()



#================================Conexão com sensores=============================================

def receiveDataFromSensorTemp():
   
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channelTemp = connection.channel()
    channelTemp.queue_declare(queue='sensor_Temperatura')

    def callback(ch, method, properties, body):
        broadcast(body)
        datafromSensor = body.decode('ascii')
        datafromSensor= json.loads(datafromSensor)
        print("Sensor: ",datafromSensor)

        cod = datafromSensor[1]
        val = datafromSensor[2]
        sendSensorDataToAtuador(codigo = cod, valorLido = val)

    channelTemp.basic_consume(queue='sensor_Temperatura', on_message_callback=callback, auto_ack=True)    
    channelTemp.start_consuming()


def receiveDataFromSensorLum():
   
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channelLum = connection.channel()
    channelLum.queue_declare(queue='sensor_Luminosidade')

    def callback(ch, method, properties, body):
        broadcast(body)
        datafromSensor = body.decode('ascii')
        datafromSensor= json.loads(datafromSensor)
        print("Sensor: ",datafromSensor)

        cod = datafromSensor[1]
        val = datafromSensor[2]
        sendSensorDataToAtuador(codigo = cod, valorLido = val)


    channelLum.basic_consume(queue='sensor_Luminosidade', on_message_callback=callback, auto_ack=True)
    
    channelLum.start_consuming()


def receiveDataFromSensorEnv():
   
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channelEnv = connection.channel()
    channelEnv.queue_declare(queue='sensor_Envasao')

    def callback(ch, method, properties, body):
        broadcast(body)
        datafromSensor = body.decode('ascii')
        datafromSensor= json.loads(datafromSensor)
        print("Sensor: ",datafromSensor)

        cod = datafromSensor[1]
        val = datafromSensor[2]
        sendSensorDataToAtuador(codigo = cod, valorLido = val)


    channelEnv.basic_consume(queue='sensor_Envasao', on_message_callback=callback, auto_ack=True)
    
    channelEnv.start_consuming()


th.Thread(target = receiveDataFromSensorTemp).start()
th.Thread(target = receiveDataFromSensorLum).start()
th.Thread(target = receiveDataFromSensorEnv).start()

print("Servidor Escutando....")
receiveClient()