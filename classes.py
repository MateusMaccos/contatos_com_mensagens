import Pyro4
import threading
import paho.mqtt.client as mqtt


class ServidorNomes:
    def iniciar_servidor_nomes(self, ip):
        t_servidor_nomes = threading.Thread(
            target=Pyro4.naming.startNSloop, kwargs={"host": ip}, daemon=True
        )
        t_servidor_nomes.start()


class Mensagem:
    def __init__(self, origem, destino, texto):
        self.origem = origem
        self.destino = destino
        self.texto = texto


class Usuario:
    def __init__(self, nome):
        self.user = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION1,
        )
        self.user.connect(host="test.mosquitto.org", port=1883)
        self.user.loop_start()

        self.nome = nome
        self.contatos = ["jose", "Marte", "Joao", "Carlos"]
        self.mensagens = [
            Mensagem("jose", "mateus", "OLÁ MEU BOM"),
            Mensagem("jose", "mateus", "OLÁ MEU BOM, COMO VAI?"),
        ]
        self.status = "online"

    def getNome(self):
        return self.nome

    def getStatus(self):
        return self.status

    def getContatos(self):
        return self.contatos

    def getMensagens(self):
        return self.mensagens

    def enviarMensagem(self, destino, texto):
        msg = Mensagem(self.nome, destino, texto)
        self.mensagens.append(msg)
        self.user.publish(
            topic=self.nome,
            payload=f"{destino}/" + texto,
        )

    def addContato(self, nome):
        self.contatos.append(nome)

    def removerContato(self, nome):
        self.contatos.remove(nome)

    def estaOnline(self):
        return True if self.status == "online" else False

    def alternarStatus(self):
        if self.status == "online":
            self.status = "offline"
        else:
            self.status = "online"
