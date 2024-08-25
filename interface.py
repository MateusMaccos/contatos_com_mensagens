import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from classes import Usuario, ServidorNomes
import Pyro4
import Pyro4.naming
import threading
import server
from server import ServidorDeMensagens
import time


class Aplicacao:
    def mudarTema(self):
        if self.tema == "dark":
            self.tema = "light"
        else:
            self.tema = "dark"
        self.tela.tk.call("set_theme", self.tema)

    def tela_SV_iniciar(self):
        self.tela_inicial_frame.destroy()
        self.tela.title("Cadastrar servidor de mensagens offline")
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

        self.botao_voltar = ttk.Button(
            self.frame_SV,
            text="Voltar",
            command=lambda: self.voltar_inicio(self.frame_SV),
        )
        self.botao_voltar.pack(pady=5)

    def iniciar_servidor(self, nome_sv, ip_sn, ip_sv):
        self.instancia_sv_mensagens = ServidorDeMensagens()
        t_sv = threading.Thread(
            target=server.iniciar,
            args=(nome_sv, ip_sn, ip_sv, self.instancia_sv_mensagens),
            daemon=True,
        )
        t_sv.start()

    def tela_SV_iniciado(self):
        self.tela.title("Servidor de mensagens offline")
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

            self.lbl_usuarios = tk.Label(
                self.frame_SV_iniciado, text="Usuários cadastrados:"
            )
            self.lbl_usuarios.pack(side=tk.TOP)

            self.frame_caixa_usuarios = tk.Frame(self.frame_SV_iniciado)
            self.frame_caixa_usuarios.pack(fill=tk.BOTH, expand=True)

            self.lb_usuarios = tk.Listbox(
                self.frame_caixa_usuarios, width=50, height=10
            )
            self.lb_usuarios.pack(
                side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5
            )

            # Adiciona a barra de rolagem se necessário
            scrollbar = tk.Scrollbar(
                self.frame_caixa_usuarios,
                orient=tk.VERTICAL,
                command=self.lb_usuarios.yview,
            )
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.lb_usuarios.config(yscrollcommand=scrollbar.set)

            self.carregarUsuariosCadastrados()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao localizar o servidor de nomes: {e}")

    def carregarUsuariosCadastrados(self):
        self.frame_caixa_usuarios.after(200, self.carregarUsuariosCadastrados)
        if self.lb_usuarios.size() != 0:
            self.lb_usuarios.delete(0, tk.END)
        for usuario in self.instancia_sv_mensagens.getUsuarios():
            self.lb_usuarios.insert(0, usuario)

    def tela_SN_iniciar(self):
        self.tela_inicial_frame.destroy()
        self.tela.title("Cadastrar servidor de nomes")
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

        self.botao_voltar = ttk.Button(
            self.frame_SN,
            text="Voltar",
            command=lambda: self.voltar_inicio(self.frame_SN),
        )
        self.botao_voltar.pack(pady=5)

    def tela_SN_iniciado(self):
        SN = ServidorNomes()
        ip_sn = self.entrada_IP_SN.get()
        self.tela.title("Servidor De Nomes")
        try:
            SN.iniciar_servidor_nomes(ip_sn)
        except:
            messagebox.showwarning("Aviso", "Erro ao criar servidor de nomes")

        self.frame_SN.destroy()

        self.frame_SN_iniciado = tk.Frame()
        self.frame_SN_iniciado.pack()

        self.lbl_texto = tk.Label(
            self.frame_SN_iniciado, text="Servidor de nomes iniciado"
        )
        self.lbl_texto.pack(pady=10)
        self.lbl_ip = tk.Label(self.frame_SN_iniciado, text=ip_sn)
        self.lbl_ip.pack(pady=10)

    def iniciarSNeSV(self):
        SNTeste = ServidorNomes()
        try:
            SNTeste.iniciar_servidor_nomes("192.168.1.11")
            self.iniciar_servidor("sv", "192.168.1.11", "192.168.1.11")
        except Exception as e:
            messagebox.showwarning("Aviso", f"Erro ao criar servidores: {e}")

    def tela_agenda(self):
        self.tela_inicial_frame.destroy()
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
            command=lambda: self.voltar_inicio(self.frame_agenda),
        )
        self.botao_voltar.pack(pady=5)

    def fechar_janela(self):
        self.usuario.apagarFila(self.sv_mensagens)
        self.tela.destroy()

    def tela_agenda_iniciado(self):
        self.tela.geometry("500x700")

        nome_sv = self.entrada_nome_sv.get()
        ip_sn = self.entrada_ip_sn.get()
        nome_usuario = self.entrada_nome_usuario.get()
        ip_usuario = self.entrada_ip_usuario.get()

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
                command=self.telaMensagens,
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

    def telaMensagens(self):
        try:
            selecao = self.lb_usuarios.curselection()[0]
            contatoDestino = self.lb_usuarios.get(selecao)
            self.tela_mensagens = tk.Tk()
            self.tela_mensagens.title(f"Mensagens de {contatoDestino}")
            self.tela_mensagens.geometry("500x500")
            self.tela_mensagens.tk.call("source", "azure.tcl")
            self.tela_mensagens.tk.call("set_theme", "dark")
            self.quantidadeDeMsgsReal = 0

            self.frame_scrolavel = tk.Frame(self.tela_mensagens)
            self.frame_scrolavel.pack(fill=tk.BOTH, expand=True)

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
            self.frame_mensagens = tk.Frame(self.canvas)
            self.canvas.create_window((0, 0), window=self.frame_mensagens, anchor="nw")

            self.atualiza_mensagens(contatoDestino)

            self.frame_input = tk.Frame(self.tela_mensagens)
            self.frame_input.pack(side=tk.BOTTOM, pady=5)

            self.input_mensagem = ttk.Entry(
                self.frame_input,
            )
            self.input_mensagem.pack(padx=10, side=tk.LEFT)

            self.btn_addMsg = ttk.Button(
                self.frame_input,
                text="Enviar",
                style="Accent.TButton",
                command=lambda: self.enviarMensagem(contatoDestino=contatoDestino),
            )
            self.btn_addMsg.pack(side=tk.RIGHT)
            self.atualiza_botao()

        except IndexError:
            messagebox.showwarning("Atenção", "Escolha um contato!")
        except Exception as e:
            messagebox.showwarning("Atenção", f"Não foi possível enviar mensagem! {e}")
            print(e)

    def on_canvas_configure_client(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def atualiza_botao(self):
        self.frame_input.after(200, self.atualiza_botao)
        estado_atual = "normal" if self.usuario.estaOnline() else "disabled"
        self.btn_addMsg.config(state=estado_atual)
        self.input_mensagem.config(state=estado_atual)

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
            messagebox.showerror("Erro", f"Erro ao atualizar as mensagens: {e}")

    def atualiza_mensagens(self, contatoDestino):
        try:
            self.frame_mensagens.after(200, self.atualiza_mensagens, contatoDestino)
            self.tela_mensagens.title(
                f"Mensagens de {contatoDestino} - {'Online' if self.usuario.verificaSeUsuarioEstaOnline(contatoDestino) else 'Offline'}"
            )
            self.tela.title()
            widgets = self.frame_mensagens.winfo_children()
            if len(widgets) != self.quantidadeDeMsgsReal or len(widgets) != 0:
                for widget in self.frame_mensagens.winfo_children():
                    widget.destroy()

            mensagens = self.usuario.getMensagens()
            nomeUsuarioAtual = self.usuario.getNome()

            for mensagem in mensagens:
                if (
                    mensagem.origem == contatoDestino
                    and mensagem.destino == nomeUsuarioAtual
                ):
                    self.plotarMensagem(
                        conteudo=f"{contatoDestino}: {mensagem.texto}",
                        frame=self.frame_mensagens,
                    )
                elif (
                    mensagem.origem == nomeUsuarioAtual
                    and mensagem.destino == contatoDestino
                ):
                    self.plotarMensagem(
                        conteudo=f"EU: {mensagem.texto}",
                        frame=self.frame_mensagens,
                        cor="#c3c3c3",
                    )
            self.quantidadeDeMsgsReal = len(mensagens)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar as mensagens: {e}")
            print(e)

    def enviarMensagem(self, contatoDestino):
        msg = self.input_mensagem.get()
        if msg != "":
            self.input_mensagem.delete(0, tk.END)
            self.usuario.enviarMensagem(
                destino=contatoDestino, texto=msg, sv_mensagens=self.sv_mensagens
            )
            self.plotarMensagem(
                conteudo=f"EU: {msg}", frame=self.frame_mensagens, cor="#c3c3c3"
            )
        else:
            messagebox.showwarning("Atenção", "Digite alguma coisa!")

    def plotarMensagem(self, conteudo, frame, cor="#FFFFFF"):
        self.msg_externa = ttk.Label(frame, text=conteudo, foreground=cor, anchor="w")
        self.msg_externa.pack(fill=tk.X)

    def tela_inicial(self):
        self.tela_inicial_frame = tk.Frame(self.tela)
        self.tela_inicial_frame.pack()
        self.tela.title("Menu Principal")

        self.lbl_texto_principal = tk.Label(
            self.tela_inicial_frame, text="Aplicativo de mensagens"
        )
        self.lbl_texto_principal.pack(pady=20)

        self.botao_SN = ttk.Button(
            self.tela_inicial_frame,
            text="Servidor de Nomes",
            style="Accent.TButton",
            command=self.tela_SN_iniciar,
        )
        self.botao_SN.pack(pady=(10, 10))

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

        self.botao_teste = ttk.Button(
            self.tela_inicial_frame,
            text="Botão de Teste",
            style="Accent.TButton",
            command=self.iniciarSNeSV,
        )
        self.botao_teste.pack(pady=10)

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
            self.usuario.addContato(contato)
            self.lb_usuarios.insert(tk.END, contato)
        else:
            messagebox.showwarning("Atenção", "Esse contato é você!")

    def voltar_inicio(self, frame):
        frame.destroy()
        self.tela_inicial()

    def run(self):
        self.tela = tk.Tk()
        self.tela.title("Menu Principal")
        self.tela.geometry("500x400")
        self.tela.tk.call("source", "azure.tcl")
        self.tela.tk.call("set_theme", "dark")
        self.tela_inicial()
        self.tela.mainloop()


if __name__ == "__main__":
    app = Aplicacao()
    app.run()
