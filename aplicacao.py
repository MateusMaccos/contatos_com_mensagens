import tkinter as tk
from tkinter import ttk
from telaServidorDeNomes import TelaServidorDeNomes
from telaServidorDeMensagens import TelaServidorDeMensagensOffline
from telaAgenda import TelaAgenda


class Aplicacao:
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
            command=lambda: TelaServidorDeNomes(
                tela=self.tela,
                tela_inicial=self.tela_inicial_frame,
                voltar_inicio=self.voltar_inicio,
            ).tela_SN_iniciar(),
        )
        self.botao_SN.pack(pady=(10, 10))

        self.botao_SV = ttk.Button(
            self.tela_inicial_frame,
            text="Servidor de Mensagens",
            style="Accent.TButton",
            command=lambda: TelaServidorDeMensagensOffline(
                tela=self.tela,
                tela_inicial=self.tela_inicial_frame,
                voltar_inicio=self.voltar_inicio,
            ).tela_SV_iniciar(),
        )
        self.botao_SV.pack(pady=10)

        self.botao_agenda = ttk.Button(
            self.tela_inicial_frame,
            text="Agenda de Contatos",
            style="Accent.TButton",
            command=lambda: TelaAgenda(
                tela=self.tela,
                tela_inicial=self.tela_inicial_frame,
                voltar_inicio=self.voltar_inicio,
            ).tela_agenda(),
        )
        self.botao_agenda.pack(pady=10)

    def voltar_inicio(self, frame):
        frame.destroy()
        self.tela_inicial()

    def run(self):
        self.tela = tk.Tk()
        self.tela.title("Menu Principal")
        self.tela.geometry("500x400")
        self.tela.iconbitmap("images/icon.ico")
        self.tela.tk.call("source", "azure.tcl")
        self.tela.tk.call("set_theme", "dark")
        self.tela_inicial()
        self.tela.mainloop()


if __name__ == "__main__":
    app = Aplicacao()
    app.run()
