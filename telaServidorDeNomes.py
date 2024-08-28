import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import Pyro4
import Pyro4.naming
import threading


class TelaServidorDeNomes:
    def __init__(self, tela, tela_inicial, voltar_inicio):
        self.tela = tela
        self.tela_inicial = tela_inicial
        self.voltar_inicio = voltar_inicio

    def iniciar_servidor_nomes(self, ip):
        t_servidor_nomes = threading.Thread(
            target=Pyro4.naming.startNSloop, kwargs={"host": ip}, daemon=True
        )
        t_servidor_nomes.start()

    def tela_SN_iniciar(self):
        self.tela_inicial.destroy()
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
        ip_sn = self.entrada_IP_SN.get().strip()
        self.tela.title("Servidor De Nomes")
        try:
            self.iniciar_servidor_nomes(ip_sn)
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
