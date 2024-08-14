import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from classes import Usuario, Mensagem, ServidorNomes
import Pyro4
import Pyro4.naming
import threading
import server


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

            self.lbl_texto = tk.Label(
                self.frame_SV_iniciado, text="Servidor de mensagens iniciado"
            )
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
        try:
            SN.iniciar_servidor_nomes(self.entrada_IP_SN.get())
        except:
            messagebox.showwarning("Aviso", "Erro ao criar servidor de nomes")

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

        self.lbl_nome_usuario = tk.Label(self.frame_agenda, text="Nome de usuario")
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
        self.usuario = Usuario(nome_usuario)

        self.frame_agenda.destroy()

        self.sv_mensagens = Pyro4.Proxy("PYRONAME:" + nome_sv + "@" + ip_sn + ":9090")

        self.sv_mensagens.addUsuario(nome_usuario)

        self.frame_agenda_iniciada = tk.Frame()
        self.frame_agenda_iniciada.pack()

        self.cabecalho = tk.Frame(self.frame_agenda_iniciada)
        self.cabecalho.pack()

        self.botao_adicionar = ttk.Button(
            self.cabecalho,
            text="Adicionar contato",
            style="Accent.TButton",
            command=self.telaAdicionarContato,
        )
        self.botao_adicionar.pack(pady=10, side=tk.LEFT)

        self.frame_status = tk.Frame(self.cabecalho)
        self.frame_status.pack(side=tk.RIGHT)

        self.statusSwitch = tk.BooleanVar()
        self.statusSwitch.set(self.usuario.getStatus() == "online")
        self.switch = ttk.Checkbutton(
            self.frame_status,
            text=self.usuario.getStatus(),
            style="Switch.TCheckbutton",
            command=self.atualizarStatus,
            variable=self.statusSwitch,
        )
        self.switch.pack()

        self.lbl_texto = tk.Label(self.cabecalho, text="Contatos")
        self.lbl_texto.pack(pady=10, padx=50, side=tk.RIGHT)

        self.frame_contatos = tk.Frame()
        self.frame_contatos.pack()

        frame_caixa_usuarios = tk.Frame(self.frame_contatos)
        frame_caixa_usuarios.pack(fill=tk.BOTH, expand=True)

        self.lb_usuarios = tk.Listbox(frame_caixa_usuarios, width=50, height=10)
        self.lb_usuarios.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Adiciona a barra de rolagem se necessário
        scrollbar = tk.Scrollbar(
            frame_caixa_usuarios, orient=tk.VERTICAL, command=self.lb_usuarios.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.lb_usuarios.config(yscrollcommand=scrollbar.set)

        self.botao_adicionar = ttk.Button(
            self.frame_contatos,
            text="Enviar Mensagem",
            style="Accent.TButton",
            command=self.telaMensagens,
        )
        self.botao_adicionar.pack(pady=10, side=tk.LEFT)

    def atualizarStatus(self):
        self.switch.destroy()
        self.usuario.alternarStatus()
        self.statusSwitch.set(self.usuario.getStatus() == "online")
        self.switch = ttk.Checkbutton(
            self.frame_status,
            text=self.usuario.getStatus(),
            style="Switch.TCheckbutton",
            command=self.atualizarStatus,
            variable=self.statusSwitch,
        )
        self.switch.pack()

    def telaMensagens(self):
        nomeContato = self.usuario.getContatos()[self.lb_usuarios.curselection()[0]]
        self.tela_cadastro = tk.Tk()
        self.tela_cadastro.title(f"Mensagens de {nomeContato}")
        self.tela_cadastro.geometry("500x500")
        self.tela_cadastro.tk.call("source", "azure.tcl")
        self.tela_cadastro.tk.call("set_theme", "dark")

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

    def telaAdicionarContato(self):
        self.tela_cadastro = tk.Tk()
        self.tela_cadastro.title("Cadastrar")
        self.tela_cadastro.geometry("500x500")
        self.tela_cadastro.tk.call("source", "azure.tcl")
        self.tela_cadastro.tk.call("set_theme", "dark")

        self.frame_cadastro = tk.Frame(self.tela_cadastro)
        self.frame_cadastro.pack()

        self.entrada_nome_contato = ttk.Entry(self.frame_cadastro)
        self.entrada_nome_contato.pack(pady=5, padx=10, side=tk.LEFT)

        self.botao_adicionar = ttk.Button(
            self.frame_cadastro,
            text="Adicionar contato",
            style="Accent.TButton",
            command=self.adicionarContato,
        )
        self.botao_adicionar.pack(pady=10, side=tk.LEFT)

    def adicionarContato(self):
        contato = self.entrada_nome_contato.get()
        self.usuario.addContato(contato)
        self.lb_usuarios.insert(tk.END, contato)

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
