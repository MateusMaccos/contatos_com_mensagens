import Pyro4
import paho.mqtt.client as mqtt
from classes import Usuario, Mensagem


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class ServidorDeMensagens(object):
    def __init__(self):
        self.server = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION1,
        )
        self.server.on_message = self.aoReceberMensagem
        self.server.connect(host="test.mosquitto.org", port=1883)
        self.server.loop_start()
        self.usuarios = []

    def aoReceberMensagem(self, client, userdata, message):
        mensagemNaoTratada = message.payload.decode()
        contatoDestino = str(mensagemNaoTratada).split("/")[0]
        mensagemTratada = str(mensagemNaoTratada).split("/")[1]
        for usuario in self.usuarios:
            usuarioAtual = usuario.getNome()
            usuarioOrigem = message.topic
            if usuarioAtual == contatoDestino or usuarioAtual == usuarioOrigem:
                usuario.mensagens.append(
                    Mensagem(usuarioOrigem, contatoDestino, mensagemTratada)
                )

    def getMensagensDoUsuario(self, usuarioBuscado):
        for usuario in self.usuarios:
            if usuario.getNome() == usuarioBuscado:
                return usuario.getMensagensPorLista()

    def addUsuario(self, user):
        usuarioNovo = Usuario(user)
        print(usuarioNovo.getNome())
        self.usuarios.append(usuarioNovo)
        self.server.subscribe(user)

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
