import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import Pyro4
import Pyro4.naming
from classes import Usuario
from telaMensagensDiretas import telaMensagensDiretas


class TelaAgenda:

    def __init__(self, tela, tela_inicial, voltar_inicio):
        self.tela_inicial = tela_inicial
        self.tela = tela
        self.voltar_inicio = voltar_inicio
        self.telas_mensagens_abertas = []

    def tela_agenda(self):
        self.tela_inicial.destroy()
        self.tela.title("Cadastrar usuário")
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

        self.lbl_nome_usuario = tk.Label(self.frame_agenda, text="Nome do usuário")
        self.lbl_nome_usuario.pack(pady=5)

        self.entrada_nome_usuario = ttk.Entry(self.frame_agenda)
        self.entrada_nome_usuario.pack(pady=5)

        self.lbl_ip_usuario = tk.Label(self.frame_agenda, text="IP do usuário")
        self.lbl_ip_usuario.pack(pady=5)

        self.entrada_ip_usuario = ttk.Entry(self.frame_agenda)
        self.entrada_ip_usuario.pack(pady=5)

        self.botao_iniciar = ttk.Button(
            self.frame_agenda,
            text="Iniciar Agenda",
            style="Accent.TButton",
            command=self.tela_agenda_iniciado,
        )
        self.botao_iniciar.pack(pady=10)

        self.botao_voltar = ttk.Button(
            self.frame_agenda,
            text="Voltar",
            command=lambda: self.voltar_inicio(self.frame_SN),
        )
        self.botao_voltar.pack(pady=5)

    def fechar_janela(self):
        self.usuario.removerUsuarioDoServidor(self.sv_mensagens)
        self.usuario.apagarFila(self.sv_mensagens)
        for tela_mensagens in self.telas_mensagens_abertas:
            tela_mensagens.fechar_janela()
        self.tela.destroy()

    def abrir_tela_mensagens(self):
        try:
            selecao = self.lb_usuarios.curselection()[0]
            contato = self.lb_usuarios.get(selecao)
            telaDeMensagens = telaMensagensDiretas(
                usuario=self.usuario, sv_mensagens=self.sv_mensagens, classe_agenda=self
            )
            self.telas_mensagens_abertas.append(telaDeMensagens)
            telaDeMensagens.telaMensagens(contato)
        except IndexError:
            messagebox.showwarning("Atenção", "Selecione um contato!")

    def tela_agenda_iniciado(self):
        self.tela.geometry("500x700")

        nome_sv = self.entrada_nome_sv.get()
        ip_sn = self.entrada_ip_sn.get().strip()
        nome_usuario = self.entrada_nome_usuario.get()
        ip_usuario = self.entrada_ip_usuario.get().strip()

        self.usuario = Usuario(nome_usuario, ip_sn, ip_usuario)

        self.tela.title(f"Agenda - {nome_usuario}")

        self.frame_agenda.destroy()

        try:
            self.sv_mensagens = Pyro4.Proxy(
                "PYRONAME:" + nome_sv + "@" + ip_sn + ":9090"
            )
            self.sv_mensagens.addUsuario(nome_usuario)

            self.frame_agenda_iniciada = tk.Frame()
            self.frame_agenda_iniciada.pack()
            self.tela.protocol(name="WM_DELETE_WINDOW", func=self.fechar_janela)
            self.cabecalho = tk.Frame(self.frame_agenda_iniciada)
            self.cabecalho.pack()

            self.botao_adicionar = ttk.Button(
                self.cabecalho,
                text="Adicionar contato",
                style="Accent.TButton",
                command=self.telaAdicionarContato,
            )
            self.botao_adicionar.pack(pady=10, side=tk.LEFT)

            self.frame_apagar = tk.Frame(self.cabecalho)
            self.frame_apagar.pack(side=tk.RIGHT)

            self.botao_adicionar = ttk.Button(
                self.frame_apagar,
                text="Apagar Contato",
                command=self.removerContato,
            )
            self.botao_adicionar.pack(pady=10, side=tk.RIGHT)

            self.lbl_texto = tk.Label(self.cabecalho, text="Contatos")
            self.lbl_texto.pack(pady=10, padx=50, side=tk.RIGHT)

            self.frame_contatos = tk.Frame(self.frame_agenda_iniciada)
            self.frame_contatos.pack()

            frame_caixa_usuarios = tk.Frame(self.frame_contatos)
            frame_caixa_usuarios.pack(fill=tk.BOTH, expand=True)

            self.lb_usuarios = tk.Listbox(frame_caixa_usuarios, width=50, height=10)
            self.lb_usuarios.pack(
                side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5
            )

            for contato in self.usuario.getContatos():
                self.lb_usuarios.insert(0, contato)

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
                command=self.abrir_tela_mensagens,
            )
            self.botao_adicionar.pack(pady=10, side=tk.RIGHT)

            self.frame_switch = tk.Frame(self.frame_contatos)
            self.frame_switch.pack(side=tk.LEFT)

            self.statusSwitch = tk.BooleanVar()
            self.statusSwitch.set(self.usuario.getStatus() == "online")
            self.switch = ttk.Checkbutton(
                self.frame_switch,
                text=self.usuario.getStatus(),
                style="Switch.TCheckbutton",
                command=self.atualizarStatus,
                variable=self.statusSwitch,
            )
            self.switch.pack()

            self.cabecalho_msgs_novas = tk.Frame()
            self.cabecalho_msgs_novas.pack()

            separator = tk.Frame(
                self.frame_agenda_iniciada, height=2, bd=1, relief=tk.SUNKEN
            )
            separator.pack(fill="x", padx=5, pady=5)

            self.lbl_texto = tk.Label(self.cabecalho_msgs_novas, text="Mensagens novas")
            self.lbl_texto.pack(pady=5, padx=5)

            separator = tk.Frame(
                self.cabecalho_msgs_novas, height=2, bd=1, relief=tk.SUNKEN
            )
            separator.pack(fill="x", padx=5, pady=5)

            self.frame_scrolavel = tk.Frame()
            self.frame_scrolavel.pack()

            # Cria um Canvas
            self.canvas = tk.Canvas(self.frame_scrolavel)
            self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Adiciona barras de rolagem
            self.scrollbar_vertical = tk.Scrollbar(
                self.frame_scrolavel, orient=tk.VERTICAL, command=self.canvas.yview
            )
            self.scrollbar_vertical.pack(side=tk.RIGHT, fill=tk.Y)

            # Configuração do Canvas
            self.canvas.configure(
                yscrollcommand=self.scrollbar_vertical.set,
            )
            self.canvas.bind("<Configure>", self.on_canvas_configure_client)

            # Adiciona um frame para o conteúdo
            self.frame_mensagens_novas = tk.Frame(self.canvas)
            self.canvas.create_window(
                (0, 0), window=self.frame_mensagens_novas, anchor="nw"
            )
            self.quantidadeDeMsgsNovas = 0
            self.atualiza_mensagens_novas()

        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível conectar ao servidor:{e}")

    def atualizarStatus(self):
        self.switch.destroy()
        self.usuario.alternarStatus(self.sv_mensagens)
        self.statusSwitch.set(self.usuario.getStatus() == "online")
        self.switch = ttk.Checkbutton(
            self.frame_switch,
            text=self.usuario.getStatus(),
            style="Switch.TCheckbutton",
            command=self.atualizarStatus,
            variable=self.statusSwitch,
        )
        self.switch.pack()

    def on_canvas_configure_client(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def atualiza_mensagens_novas(self):
        try:
            self.frame_mensagens_novas.after(200, self.atualiza_mensagens_novas)
            widgets = self.frame_mensagens_novas.winfo_children()
            if len(widgets) != self.quantidadeDeMsgsNovas or len(widgets) != 0:
                for widget in self.frame_mensagens_novas.winfo_children():
                    widget.destroy()
            mensagens = self.usuario.getMensagens()
            nomeUsuarioAtual = self.usuario.getNome()
            contador = 0
            for mensagem in mensagens:
                if mensagem.destino == nomeUsuarioAtual:
                    self.plotarMensagem(
                        conteudo=f"{mensagem.origem}: {mensagem.texto}",
                        frame=self.frame_mensagens_novas,
                    )
                    contador = contador + 1
            self.quantidadeDeMsgsNovas = contador
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar as mensagens novas: {e}")

    def plotarMensagem(self, conteudo, frame, cor="#FFFFFF"):
        self.msg_externa = ttk.Label(frame, text=conteudo, foreground=cor, anchor="w")
        self.msg_externa.pack(fill=tk.X)

    def telaAdicionarContato(self):
        self.tela_cadastro = tk.Tk()
        self.tela_cadastro.title("Cadastrar")
        self.tela_cadastro.geometry("500x100")
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
        if contato in self.usuario.contatos:
            messagebox.showwarning("Atenção", "Esse contato já existe na sua lista!")
        elif contato != self.usuario.nome:
            try:
                self.usuario.ns.lookup(contato)
                self.usuario.addContato(contato)
                self.lb_usuarios.insert(tk.END, contato)
            except:
                messagebox.showwarning("Atenção", "Esse usuário não existe!")

        else:
            messagebox.showwarning("Atenção", "Esse contato é você!")

    def removerContato(self):
        try:
            selecao = self.lb_usuarios.curselection()[0]
            contatoSelecionado = self.lb_usuarios.get(selecao)
            self.usuario.removerContato(contatoSelecionado)
            self.lb_usuarios.delete(tk.ANCHOR)
        except IndexError:
            messagebox.showwarning("Atenção", "Escolha um contato!")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível apagar esse contato! {e}")
