import pika


class BrokerMensagens:
    def __init__(self, rabbitmq_host, username, password, vhost):
        self.connection_params = pika.ConnectionParameters(
            host=rabbitmq_host,
            credentials=pika.PlainCredentials(username, password),
            virtual_host=vhost,
        )
        self.connection = pika.BlockingConnection(self.connection_params)
        self.channel = self.connection.channel()

    def criar_fila(self, queue):
        queue_name = queue
        self.channel.queue_declare(queue=queue_name)

    def enviar_mensagem_ao_usuario(self, queue, message):
        queue_name = queue
        self.channel.basic_publish(exchange="", routing_key=queue_name, body=message)
        print(f"Enviada mensagem para {queue_name}")

    def receber_mensagens_do_usuario(self, queue):
        mensagens = []
        while True:
            method_frame, header_frame, body = self.channel.basic_get(
                queue=queue, auto_ack=False
            )

            if method_frame:
                msg = body.decode("utf-8")
                print(f"Mensagem recebida: {msg}")
                self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                mensagens.append(msg)
            else:
                print("Nenhuma mensagem disponível na fila.")
                break

        return mensagens

    def encerrar_conexao(self):
        self.connection.close()


if __name__ == "__main__":
    middleware = BrokerMensagens(
        rabbitmq_host="jackal-01.rmq.cloudamqp.com",
        username="unygrgmp",
        password="jRtbPlY8eHLOXUIFP8Oz06GaIVMAXtjh",
        vhost="unygrgmp",
    )

    # Criar uma fila para um usuário específico
    middleware.criar_fila(queue="user_123")

    # Enviar uma mensagem para o usuário 123
    middleware.enviar_mensagem_ao_usuario(queue="user_123", message="Hello User 123!")
    middleware.enviar_mensagem_ao_usuario(queue="user_123", message="Hello Users!")
    middleware.enviar_mensagem_ao_usuario(queue="user_123", message="Hey Users!")

    middleware.receber_mensagens_do_usuario(queue="user_123")

    # Fechar a conexão quando terminar
    middleware.close_connection()
