import Pyro4
import threading


@Pyro4.expose
class ChatClient:
    def __init__(self, username):
        self.username = username

    def receive_message(self, sender, message):
        print(f"Message from {sender}: {message}")

    def register(self):
        # Conecta ao servidor de nomes
        ns = Pyro4.locateNS()

        # Inicia um daemon Pyro para o cliente
        daemon = Pyro4.Daemon()

        # Registra o cliente no daemon
        uri = daemon.register(self)

        # Registra o nome do usuário no servidor de nomes
        ns.register(self.username, uri)

        print(f"{self.username} registered with URI: {uri}")

        # Inicia o loop do daemon para escutar mensagens
        daemon.requestLoop()

    def send_message(self, recipient_username, message):
        # Conecta ao servidor de nomes para buscar o destinatário
        ns = Pyro4.locateNS()
        try:
            # Obtém a URI do destinatário
            recipient_uri = ns.lookup(recipient_username)
            recipient = Pyro4.Proxy(recipient_uri)
            recipient.receive_message(self.username, message)
            print(f"Message sent to {recipient_username}: {message}")
        except Pyro4.errors.NamingError:
            print(f"User {recipient_username} not found.")


if __name__ == "__main__":
    username = input("Enter your username: ")
    client = ChatClient(username)
    thread = threading.Thread(target=client.register)
    thread.start()
    username = input("quem vc vai enviar: ")
    msg = input("o que vc vai enviar?")
    client.send_message(username, msg)
