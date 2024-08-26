import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import Pyro4
import Pyro4.naming
import threading
from server import ServidorDeMensagens
import server


class TelaServidorDeMensagensOffline:
    def __init__(self, tela, tela_inicial, voltar_inicio):
        self.tela = tela
        self.tela_inicial = tela_inicial
        self.voltar_inicio = voltar_inicio

    def tela_SV_iniciar(self):
        self.tela_inicial.destroy()
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
            command=lambda: self.voltar_inicio(self.frame_SN),
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
