#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host="jackal-01.rmq.cloudamqp.com",
        credentials=pika.PlainCredentials(
            "unygrgmp", "jRtbPlY8eHLOXUIFP8Oz06GaIVMAXtjh"
        ),
        virtual_host="unygrgmp",
    )
)
channel = connection.channel()

channel.queue_declare(queue="hello")

channel.basic_publish(exchange="", routing_key="hello", body="Hello World!")
print(" [x] Sent 'Hello World!'")
connection.close()
