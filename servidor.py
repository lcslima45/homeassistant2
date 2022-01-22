#!/usr/bin/env python
import pika
import logging

def main():
    logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
 
    # Creating an object
    logger = logging.getLogger()
 
    # Setting the threshold of logger to DEBUG
    logger.setLevel(logging.INFO)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='HomeAssistantExchange', exchange_type='fanout')

    result1 = channel.queue_declare(queue='Sensor1', exclusive=False)
    result2 = channel.queue_declare(queue='Sensor2', exclusive=False)
    result3 = channel.queue_declare(queue='Sensor2', exclusive=False)
    queue_name1 = result1.method.queue
    queue_name2 = result2.method.queue
    queue_name3 = result3.method.queue

    channel.queue_bind(exchange='HomeAssistantExchange', queue=queue_name1)
    channel.queue_bind(exchange='HomeAssistantExchange', queue=queue_name2)
    channel.queue_bind(exchange='HomeAssistantExchange', queue=queue_name2)
    print(' [*] Waiting for logs. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(" [x] %r" % body)
        logger.info(" [x] %r" % body)

    channel.basic_consume(
        queue=queue_name1, on_message_callback=callback, auto_ack=True)
    channel.basic_consume(
        queue=queue_name2, on_message_callback=callback, auto_ack=True)
    channel.basic_consume(
        queue=queue_name3, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)