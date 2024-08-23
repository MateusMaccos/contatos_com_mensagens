import pika


class MessageMiddleware:
    def __init__(self, rabbitmq_host, username, password, vhost):
        self.connection_params = pika.ConnectionParameters(
            host=rabbitmq_host,
            credentials=pika.PlainCredentials(username, password),
            virtual_host=vhost,
        )
        self.connection = pika.BlockingConnection(self.connection_params)
        self.channel = self.connection.channel()

    def create_user_queue(self, user_id):
        queue_name = f"user_{user_id}"
        self.channel.queue_declare(queue=queue_name)
        return queue_name

    def send_message_to_user(self, user_id, message):
        queue_name = f"user_{user_id}"
        self.channel.basic_publish(exchange="", routing_key=queue_name, body=message)
        print(f"Sent message to {queue_name}")

    def receive_messages_for_user(self, user_id, callback):
        queue_name = f"user_{user_id}"
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback,
            auto_ack=True,
        )
        print(f"[*] Waiting for messages for user {user_id}. To exit press CTRL+C")
        self.channel.start_consuming()

    def close_connection(self):
        self.connection.close()


# Exemplo de uso
def message_callback(ch, method, properties, body):
    print(f" [x] Received: {body.decode()}")


if __name__ == "__main__":
    middleware = MessageMiddleware(
        rabbitmq_host="jackal-01.rmq.cloudamqp.com",
        username="unygrgmp",
        password="jRtbPlY8eHLOXUIFP8Oz06GaIVMAXtjh",
        vhost="unygrgmp",
    )

    # Criar uma fila para um usuário específico
    user_queue = middleware.create_user_queue(user_id="123")

    # Enviar uma mensagem para o usuário 123
    middleware.send_message_to_user(user_id="123", message="Hello User 123!")

    # Consumir mensagens da fila do usuário 123
    middleware.receive_messages_for_user(user_id="123", callback=message_callback)

    # Fechar a conexão quando terminar
    middleware.close_connection()
