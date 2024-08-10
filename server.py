import Pyro4


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class ServidorDeMensagens(object):
    def testarSM(self):
        print("TESTE")


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
