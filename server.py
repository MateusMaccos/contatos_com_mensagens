import Pyro4
from classes import Usuario, Mensagem


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class ServidorDeMensagens(object):
    def __init__(self):
        self.usuarios = []

    def addUsuario(self, user):
        usuarioNovo = Usuario(user)
        self.usuarios.append(usuarioNovo)
        print(usuarioNovo.getNome())

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
