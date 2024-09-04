import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import Pyro4


class telaMensagensDiretas:

    def __init__(self, usuario, sv_mensagens, classe_agenda):
        self.usuario = usuario
        self.sv_mensagens = sv_mensagens
        self.classe_agenda = classe_agenda

    def fechar_janela(self):
        self.classe_agenda.telas_mensagens_abertas.remove(self)
        self.tela_mensagens.destroy()

    def telaMensagens(self, contatoDestino):
        try:
            self.tela_mensagens = tk.Tk()
            self.tela_mensagens.title(f"Mensagens de {contatoDestino}")
            self.tela_mensagens.iconbitmap("images/icon.ico")
            self.tela_mensagens.geometry("500x500")
            self.tela_mensagens.protocol(
                name="WM_DELETE_WINDOW", func=self.fechar_janela
            )
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
            self.tela_mensagens.bind(
                "<Return>",
                func=lambda event: self.enviarMensagem(contatoDestino=contatoDestino),
            )

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

    def on_canvas_configure_client(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def atualiza_botao(self):
        self.frame_input.after(200, self.atualiza_botao)
        estado_atual = "normal" if self.usuario.estaOnline() else "disabled"
        self.btn_addMsg.config(state=estado_atual)
        self.input_mensagem.config(state=estado_atual)

    def atualiza_mensagens(self, contatoDestino):
        try:
            self.frame_mensagens.after(200, self.atualiza_mensagens, contatoDestino)
            self.tela_mensagens.title(
                f"Mensagens de {contatoDestino} - {'Online' if self.usuario.verificaSeUsuarioEstaOnline(contatoDestino) else 'Offline'}"
            )
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
        except Pyro4.errors.CommunicationError:
            self.fechar_janela()
            messagebox.showerror("Erro", f"{contatoDestino} desconectou da aplicação!")
        except Exception as e:
            self.fechar_janela()
            messagebox.showerror(
                "Erro", f"Erro ao atualizar as mensagens do usuário: {e}"
            )

    def enviarMensagem(self, contatoDestino):
        msg = self.input_mensagem.get()
        if msg != "":
            self.input_mensagem.delete(0, tk.END)
            try:
                self.usuario.enviarMensagem(
                    destino=contatoDestino, texto=msg, sv_mensagens=self.sv_mensagens
                )
            except Pyro4.errors.NamingError:
                messagebox.showerror(
                    "Erro", f"Usuário {contatoDestino} não encontrado."
                )
            except Exception as e:
                messagebox.showerror("Erro", f"Erro inesperado ocorreu: {e}")
            self.plotarMensagem(
                conteudo=f"EU: {msg}", frame=self.frame_mensagens, cor="#c3c3c3"
            )
        else:
            messagebox.showwarning("Atenção", "Digite alguma coisa!")

    def plotarMensagem(self, conteudo, frame, cor="#FFFFFF"):
        self.msg_externa = ttk.Label(frame, text=conteudo, foreground=cor, anchor="w")
        self.msg_externa.pack(fill=tk.X)
