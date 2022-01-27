from concurrent import futures
import time
import grpc
import atuador_pb2_grpc as pb2_grpc
import atuador_pb2 as pb2
import json

class atuadorServiceServicer(pb2_grpc.atuadorServiceServicer):
    def __init__(self):
        self.codigo = 1000
        self.nome = "Ar-condicionado"
    
    def sendInfo(self, request, context):
        global Status
        comando = request.info
        if comando == 1:
            Status = "Ligado"
        else:
            Status = "Desligado"
        
        print("Status atual: ",Status)
        
        response = pb2.status(codigo = self.codigo, nome = self.nome, mensagem = Status)
        return response

server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
pb2_grpc.add_atuadorServiceServicer_to_server(atuadorServiceServicer(), server)
print("Ar-condicionado connectado")
server.add_insecure_port('[::]:50051')
server.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    server.stop()