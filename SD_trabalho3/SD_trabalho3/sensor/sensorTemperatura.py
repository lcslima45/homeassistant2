import json
import time
import random
import pika
import threading as th


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='sensor_Temperatura')

codigo = 1000
id = "Temp"


     
    

print("Iniciou a leitura")
while True:
    leitura = random.random()*100
    horaLeitura = time.localtime() # get struct_time
    horaStr = time.strftime("%m/%d/%Y, %H:%M:%S", horaLeitura)

    dadosLeitura = [id, codigo, leitura, horaStr]
    print(dadosLeitura)
    data_toSend = json.dumps(dadosLeitura)
    channel.basic_publish(exchange='', routing_key='sensor_Temperatura', body=data_toSend)

    time.sleep(5)

connection.close()

"""
 channel.queue_declare(queue='nemo')
        channel.basic_publish(exchange='',
                      routing_key='nemo',
                      body='Nao tem FOGO!!!')
        print(" [x] Sent 'Nao tem FOGO'")
"""