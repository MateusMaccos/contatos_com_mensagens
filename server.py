import Pyro4
from classes import Usuario, Mensagem, BrokerMensagens


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class ServidorDeMensagens(object):
    def __init__(self):
        self.usuarios = []
        self.broker = BrokerMensagens(
            rabbitmq_host="jackal-01.rmq.cloudamqp.com",
            username="unygrgmp",
            password="jRtbPlY8eHLOXUIFP8Oz06GaIVMAXtjh",
            vhost="unygrgmp",
        )

    def enviarMensagemParaOffline(self, destino, msg):
        self.broker.enviar_mensagem_ao_usuario(destino, msg)

    def getMensagensDoUsuario(self, usuarioBuscado):
        mensagens = []
        for mensagem in self.broker.receber_mensagens_do_usuario(usuarioBuscado):
            origem = str(mensagem).split(":")[0]
            conteudo = str(mensagem).split(":")[1]
            mensagens.append([origem, usuarioBuscado, conteudo])
        return mensagens

    def addUsuario(self, user):
        usuarioNovo = Usuario(user)
        print(usuarioNovo.getNome())
        self.broker.criar_fila(user)
        self.usuarios.append(usuarioNovo)

    def getTodosUsuarios(self):
        nomes = []
        for usuario in self.usuarios:
            nomes.append(usuario.nome)
        return nomes


def iniciar(nomeSV, ipNS, ipSV):
    daemon = Pyro4.Daemon(host=ipSV)
    try:
        ns = Pyro4.locateNS(host=ipNS, port=9090)
        uri = daemon.register(ServidorDeMensagens)
        ns.register(nomeSV, uri)
        print(ipSV)
        daemon.requestLoop()
    except Exception as e:
        print(e)
