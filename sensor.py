import time
import random
import pika
a = True
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='HomeAssistantExchange', exchange_type='fanout')
channel.queue_declare(queue='Sensor1')

count = 0 
while a:
    n = random.randint(0,20)
    print(n)
  
    if n==15:
        channel.basic_publish(exchange='HomeAssistantExchange',
                      routing_key='Sensor1',
                      body='Sensor1 - FOGO!!!')
        print(" [x] Sent 'FOGO'")
        count = count + 1
        if count == 5:
            a = False
            connection.close()
       
    else:
        channel.basic_publish(exchange='HomeAssistantExchange',
                      routing_key='Sensor1',
                      body='Sensor1 - Nao tem FOGO!!!')
        print(" [x] Sent 'Nao tem FOGO'")

        
    time.sleep(5)   