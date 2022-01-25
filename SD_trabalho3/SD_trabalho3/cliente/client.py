import socket
import threading
import json
import time

from Home_Assistent.serverdefinitivo import Arcondicionado

print('Connectando ao servidor...')
time.sleep(3)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5000))
signature = client.getsockname()

print("Para enviar comando para habilitar ou desabilitar os atuadore")
print("Primeiro digte o codigo em seguida o comando")
print("1-para Habilira e 0-para desabilitar")
print("Codigos dos Atuadores")
print("1000 - Arcondicionado")
print("2000 - Lampada")
print("3000 - Alarme")

time.sleep(5)

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            print(message)

        except:
            print("Erro")
            client.close()
            break
def write():
    while True:
        cod = input()
        com = input()
        
        message = [signature, cod, com]
        jsonMessage = json.dumps(message)
        client.send(jsonMessage.encode('ascii'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
