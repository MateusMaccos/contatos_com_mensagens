#!/usr/bin/env python
import pika, sys, os


def main():
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

    # channel.queue_delete(queue="hello")
    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}")
        # channel.basic_cancel(consumer_tag="cliente")

    channel.basic_consume(
        queue="hello",
        on_message_callback=callback,
        auto_ack=True,
        consumer_tag="cliente",
    )

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
