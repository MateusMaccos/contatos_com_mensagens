import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import Pyro4
import Pyro4.naming
import threading


class ServidorNomes:
    def iniciar_servidor_nomes(self, ip):
        try:
            t_servidor_nomes = threading.Thread(
                target=Pyro4.naming.startNSloop, kwargs={"host": ip}, daemon=True
            )
            t_servidor_nomes.start()
        except:
            messagebox.showwarning("Aviso", "Erro ao criar servidor de nomes")


class Aplicacao:
    def __init__(self):
        self.usuarios = []

    def mudarTema(self):
        if self.tema == "dark":
            self.tema = "light"
        else:
            self.tema = "dark"
        self.tela.tk.call("set_theme", self.tema)

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

    def run(self):
        self.tela = tk.Tk()
        self.tela.title("Agenda")
        self.tela.geometry("1200x500")
        self.tela.tk.call("source", "azure.tcl")
        self.tela.tk.call("set_theme", "dark")

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

        self.botao_iniciar = ttk.Button(
            self.frame_SN,
            text="Limpar Tela",
            style="Accent.TButton",
            command=self.frame_SN.destroy,
        )
        self.botao_iniciar.pack(pady=5)

        self.tela.mainloop()


if __name__ == "__main__":
    app = Aplicacao()
    app.run()
