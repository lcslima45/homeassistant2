import time
import random
import pika
a = True
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='HomeAssistantExchange', exchange_type='fanout')
channel.queue_declare(queue='Sensor3')

count = 0 
while a:
    n = random.randint(0,20)
    print(n)
  
    if n==15:
        channel.basic_publish(exchange='HomeAssistantExchange',
                      routing_key='Sensor3',
                      body='Sensor3 - LUZ!!!')
        print(" [x] Sent 'LUZ'")
        count = count + 1
        if count == 5:
            a = False
            connection.close()
       
    else:
        channel.basic_publish(exchange='HomeAssistantExchange',
                      routing_key='Sensor3',
                      body='Sensor3 - ESCURO!!!')
        print(" [x] Sent 'ESCURO'")

        
    time.sleep(5)