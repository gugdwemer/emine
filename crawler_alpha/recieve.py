#!/usr/bin/env python3

import pika
import json
from functions import writetodb

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='tweets')


def callback(ch, method, properties, body):
    body = json.loads(str(body, 'utf-8'))
    print(" [x] Received %r" % body)
    writetodb(body)


channel.basic_consume(callback,
                      queue='tweets',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
