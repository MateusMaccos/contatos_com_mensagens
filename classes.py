import Pyro4
import threading
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

    def enviar_mensagem_ao_usuario(self, origem, queue, message):
        queue_name = queue
        self.channel.basic_publish(
            exchange="", routing_key=queue_name, body=f"{origem}:{message}"
        )

    def receber_mensagens_do_usuario(self, queue):
        mensagens = []
        while True:
            method_frame, header_frame, body = self.channel.basic_get(
                queue=queue, auto_ack=False
            )

            if method_frame:
                msg = body.decode("utf-8")
                self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                mensagens.append(msg)
            else:
                break

        return mensagens

    def encerrar_conexao(self):
        self.connection.close()


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


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Usuario(object):
    def __init__(self, nome, svNomes, ipUsuario):
        self.nome = nome
        self.ipSvNomes = svNomes
        self.ipUsuario = ipUsuario
        self.register()
        self.contatos = []
        self.mensagens = []
        self.status = "online"

    def register(self):
        self.ns = Pyro4.locateNS(host=self.ipSvNomes, port=9090)

        daemon = Pyro4.Daemon(host=self.ipUsuario)

        uri = daemon.register(self)

        self.ns.register(self.nome, uri)

        threadUsuario = threading.Thread(
            target=daemon.requestLoop,
            daemon=True,
        )
        threadUsuario.start()

    def getNome(self):
        return self.nome

    def getStatus(self):
        return self.status

    def getContatos(self):
        return self.contatos

    def getMensagens(self):
        return self.mensagens

    def getMensagensPorLista(self):
        listaMsg = []
        for mensagem in self.mensagens:
            listaMsg.append([mensagem.origem, mensagem.destino, mensagem.texto])
        return listaMsg

    def atualizarMensagensPorLista(self, lista):
        for mensagem in lista:
            self.mensagens.append(Mensagem(mensagem[0], mensagem[1], mensagem[2]))

    def receberMensagem(self, origem, texto):
        self.mensagens.append(Mensagem(origem, self.nome, texto))

    def enviarMensagem(self, destino, texto, sv_mensagens):
        msg = Mensagem(self.nome, destino, texto)
        self.mensagens.append(msg)
        try:
            destino_uri = self.ns.lookup(destino)
            destino_instancia = Pyro4.Proxy(destino_uri)
            if destino_instancia.estaOnline():
                destino_instancia.receberMensagem(self.nome, texto)
            else:
                sv_mensagens.enviarMensagemParaOffline(self.nome, destino, texto)
        except Exception as e:
            print(f"Error: {e}")

    def verificaSeUsuarioEstaOnline(self, usuario):
        try:
            usuario_uri = self.ns.lookup(usuario)
            usuario_instancia = Pyro4.Proxy(usuario_uri)
            if usuario_instancia.estaOnline():
                return True
            else:
                return False
        except Pyro4.errors.NamingError:
            return False
        except Exception as e:
            print(f"Error: {e}")

    def addContato(self, nome):
        self.contatos.append(nome)

    def removerContato(self, nome):
        self.contatos.remove(nome)

    def apagarFila(self, sv_mensagens):
        sv_mensagens.apagarFila(self.nome)

    def estaOnline(self):
        return True if self.status == "online" else False

    def alternarStatus(self, sv_mensagens):
        if self.status == "online":
            self.status = "offline"
        else:
            mensagensDoServidor = sv_mensagens.getMensagensDoUsuario(self.nome)
            self.atualizarMensagensPorLista(mensagensDoServidor)
            self.status = "online"
