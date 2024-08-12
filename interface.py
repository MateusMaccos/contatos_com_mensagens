import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import Pyro4
import Pyro4.naming
import threading
import server
import paho.mqtt.client as mqtt

class ServidorNomes:
    def iniciar_servidor_nomes(self, ip):
        try:
            t_servidor_nomes = threading.Thread(
                target=Pyro4.naming.startNSloop, kwargs={"host": ip}, daemon=True
            )
            t_servidor_nomes.start()
        except:
            messagebox.showwarning("Aviso", "Erro ao criar servidor de nomes")

class Mensagem:
    def __init__(self,origem,destino,texto):
        self.origem = origem
        self.destino = destino
        self.texto = texto


class Usuario:
    def __init__(self,nome):
        self.user = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION1,
        )
        self.user.connect(host="test.mosquitto.org", port=1883)
        self.user.loop_start()

        self.nome = nome
        self.contatos = []
        self.mensagens=[]
    def getNome(self):
        return self.nome
    def enviarMensagem(self,origem,destino,texto):
        msg = Mensagem(origem,destino,texto)
        self.mensagens.append(msg)
    def addContato(self,nome):
        self.contatos.append(nome)
    def removerContato(self,nome):
        self.contatos.remove(nome)

class Aplicacao:
    def mudarTema(self):
        if self.tema == "dark":
            self.tema = "light"
        else:
            self.tema = "dark"
        self.tela.tk.call("set_theme", self.tema)

    def tela_SV_iniciar(self):
        self.tela_inicial_frame.destroy()

        self.frame_SV = tk.Frame(self.tela)
        self.frame_SV.pack()

        self.lbl_texto_ip_sn = tk.Label(self.frame_SV, text="IP do Servidor de Nomes:")
        self.lbl_texto_ip_sn.pack(pady=5)

        self.entrada_IP_SN = ttk.Entry(self.frame_SV)
        self.entrada_IP_SN.pack(pady=5)

        self.lbl_texto_cadastro = tk.Label(
            self.frame_SV, text="Nome para cadastrar Servidor"
        )
        self.lbl_texto_cadastro.pack(pady=5)

        self.entrada_nome_sv = ttk.Entry(self.frame_SV)
        self.entrada_nome_sv.pack(pady=5)

        self.lbl_texto_ip_sv = tk.Label(self.frame_SV, text="IP do Servidor")
        self.lbl_texto_ip_sv.pack(pady=5)

        self.entrada_ip_sv = ttk.Entry(self.frame_SV)
        self.entrada_ip_sv.pack(pady=5)

        self.botao_iniciar = ttk.Button(
            self.frame_SV,
            text="Iniciar Servidor",
            style="Accent.TButton",
            command=self.tela_SV_iniciado,
        )
        self.botao_iniciar.pack(pady=10)

    def iniciar_servidor(self, nome_sv, ip_sn, ip_sv):
        t_sv = threading.Thread(
            target=server.iniciar,
            args=(nome_sv, ip_sn, ip_sv),
            daemon=True,
        )
        t_sv.start()

    def tela_SV_iniciado(self):
        ip_sn = self.entrada_IP_SN.get()
        ip_sv = self.entrada_ip_sv.get()
        nome_sv = self.entrada_nome_sv.get()
        try:
            Pyro4.locateNS(host=ip_sn, port=9090)
            self.iniciar_servidor(nome_sv, ip_sn, ip_sv)
            self.frame_SV.destroy()

            self.frame_SV_iniciado = tk.Frame(self.tela)
            self.frame_SV_iniciado.pack()

            self.lbl_texto = tk.Label(self.frame_SV_iniciado, text="Servidor de mensagens iniciado")
            self.lbl_texto.pack(pady=10)

            self.lbl_ip_sv = tk.Label(self.frame_SV_iniciado, text=f"IP: {ip_sv}")
            self.lbl_ip_sv.pack(pady=10)

            self.lbl_nome_sv = tk.Label(self.frame_SV_iniciado, text=f"Nome: {nome_sv}")
            self.lbl_nome_sv.pack(pady=10)

            # self.lbl_usuarios = tk.Label(self.frame_SV_iniciado, text="Usuários cadastrados:")
            # self.lbl_usuarios.pack(side=tk.TOP)

            # frame_caixa_usuarios = tk.Frame(self.frame_SV_iniciado)
            # frame_caixa_usuarios.pack(fill=tk.BOTH, expand=True)

            # self.lb_usuarios = tk.Listbox(frame_caixa_usuarios, width=50, height=10)
            # self.lb_usuarios.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

            # # Adiciona a barra de rolagem se necessário
            # scrollbar = tk.Scrollbar(frame_caixa_usuarios, orient=tk.VERTICAL, command=self.lb_usuarios.yview)
            # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            # self.lb_usuarios.config(yscrollcommand=scrollbar.set)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao localizar o servidor de nomes: {e}")

    def tela_SN_iniciar(self):
        self.tela_inicial_frame.destroy()

        self.frame_SN = tk.Frame(self.tela)
        self.frame_SN.pack()

        self.lbl_texto = tk.Label(self.frame_SN, text="IP do Servidor de Nomes:")
        self.lbl_texto.pack(pady=5)

        self.entrada_IP_SN = ttk.Entry(self.frame_SN)
        self.entrada_IP_SN.pack(pady=5)

        self.botao_iniciar = ttk.Button(
            self.frame_SN,
            text="Iniciar",
            style="Accent.TButton",
            command=self.tela_SN_iniciado,
        )
        self.botao_iniciar.pack(pady=5)

    def tela_SN_iniciado(self):
        SN = ServidorNomes()
        SN.iniciar_servidor_nomes(self.entrada_IP_SN.get())

        self.frame_SN.destroy()

        self.frame_SN_iniciado = tk.Frame()
        self.frame_SN_iniciado.pack()

        self.lbl_texto = tk.Label(
            self.frame_SN_iniciado, text="Servidor de nomes iniciado"
        )
        self.lbl_texto.pack(pady=10)

    def tela_agenda(self):
        self.tela_inicial_frame.destroy()
        self.frame_agenda = tk.Frame()
        self.frame_agenda.pack()

        self.lbl_texto_sv = tk.Label(self.frame_agenda, text="Nome do Servidor")
        self.lbl_texto_sv.pack(pady=5)

        self.entrada_nome_sv = ttk.Entry(self.frame_agenda)
        self.entrada_nome_sv.pack(pady=5)

        self.lbl_texto_ip_sn = tk.Label(
            self.frame_agenda, text="IP do Servidor de Nomes"
        )
        self.lbl_texto_ip_sn.pack(pady=5)

        self.entrada_ip_sn = ttk.Entry(self.frame_agenda)
        self.entrada_ip_sn.pack(pady=5)

        self.lbl_nome_usuario = tk.Label(
            self.frame_agenda, text="Nome de usuario"
        )
        self.lbl_nome_usuario.pack(pady=5)

        self.entrada_nome_usuario = ttk.Entry(self.frame_agenda)
        self.entrada_nome_usuario.pack(pady=5)

        self.botao_iniciar = ttk.Button(
            self.frame_agenda,
            text="Iniciar Agenda",
            style="Accent.TButton",
            command=self.tela_agenda_iniciado,
        )
        self.botao_iniciar.pack(pady=10)

    def tela_agenda_iniciado(self):
        nome_sv = self.entrada_nome_sv.get()
        ip_sn = self.entrada_ip_sn.get()
        nome_usuario = self.entrada_nome_usuario.get()
        usuario = Usuario(nome_usuario)

        self.frame_agenda.destroy()

        self.sv_mensagens = Pyro4.Proxy("PYRONAME:" + nome_sv + "@" + ip_sn + ":9090")

        self.sv_mensagens.addUsuario(nome_usuario)

        self.frame_agenda_iniciada = tk.Frame()
        self.frame_agenda_iniciada.pack()

        self.lbl_texto = tk.Label(
            self.frame_agenda_iniciada, text="Contatos"
        )
        self.lbl_texto.pack(pady=10)
        
        self.entrada_nome_contato = ttk.Entry(self.frame_agenda_iniciada)
        self.entrada_nome_contato.pack(pady=5)

        self.botao_iniciar = ttk.Button(
            self.frame_agenda_iniciada,
            text="Adicionar contato",
            style="Accent.TButton",
            command= lambda: self.adicionarContato(usuario),
        )
        self.botao_iniciar.pack(pady=10)

        self.lbl_usuarios = tk.Label(self.frame_agenda_iniciada, text="Contatos")
        self.lbl_usuarios.pack(side=tk.TOP)

        frame_caixa_usuarios = tk.Frame(self.frame_agenda_iniciada)
        frame_caixa_usuarios.pack(fill=tk.BOTH, expand=True)

        self.lb_usuarios = tk.Listbox(frame_caixa_usuarios, width=50, height=10)
        self.lb_usuarios.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Adiciona a barra de rolagem se necessário
        scrollbar = tk.Scrollbar(frame_caixa_usuarios, orient=tk.VERTICAL, command=self.lb_usuarios.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.lb_usuarios.config(yscrollcommand=scrollbar.set)

    def tela_inicial(self):
        self.tela_inicial_frame = tk.Frame(self.tela)
        self.tela_inicial_frame.pack()

        self.botao_SN = ttk.Button(
            self.tela_inicial_frame,
            text="Servidor de Nomes",
            style="Accent.TButton",
            command=self.tela_SN_iniciar,
        )
        self.botao_SN.pack(pady=10)

        self.botao_SV = ttk.Button(
            self.tela_inicial_frame,
            text="Servidor de Mensagens",
            style="Accent.TButton",
            command=self.tela_SV_iniciar,
        )
        self.botao_SV.pack(pady=10)

        self.botao_agenda = ttk.Button(
            self.tela_inicial_frame,
            text="Agenda de Contatos",
            style="Accent.TButton",
            command=self.tela_agenda,
        )
        self.botao_agenda.pack(pady=10)
    def adicionarContato(self,usuario):
        contato = self.entrada_nome_contato.get()
        usuario.addContato(contato)
        self.lb_usuarios.insert(0,contato)
    def run(self):
        self.tela = tk.Tk()
        self.tela.title("Agenda")
        self.tela.geometry("1200x500")
        self.tela.tk.call("source", "azure.tcl")
        self.tela.tk.call("set_theme", "dark")
        self.tela_inicial()
        self.tela.mainloop()


if __name__ == "__main__":
    app = Aplicacao()
    app.run()
