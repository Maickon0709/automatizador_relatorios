"""
interface.py

Interface gráfica simples (Tkinter) para rodar o pipeline de relatórios
sem precisar usar o terminal. A pessoa escolhe a planilha de vendas,
clica em "Gerar Relatório" e os arquivos finais (.xlsx e .png) são
salvos automaticamente em uma pasta na Área de Trabalho.
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

from main import executar_pipeline, PASTA_SAIDA_PADRAO


class AppRelatorios:
    def __init__(self, janela: tk.Tk):
        self.janela = janela
        self.caminho_planilha = None

        janela.title("Automatizador de Relatórios de Vendas")
        janela.geometry("480x280")
        janela.resizable(False, False)

        tk.Label(
            janela, text="Automatizador de Relatórios de Vendas",
            font=("Arial", 14, "bold"),
        ).pack(pady=(20, 5))

        tk.Label(
            janela, text="Selecione a planilha de vendas (.xlsx) para gerar o relatório.",
            font=("Arial", 9), fg="#555555",
        ).pack(pady=(0, 15))

        self.rotulo_arquivo = tk.Label(
            janela, text="Nenhum arquivo selecionado", font=("Arial", 9),
            fg="#888888", wraplength=440,
        )
        self.rotulo_arquivo.pack(pady=(0, 10))

        tk.Button(
            janela, text="Selecionar Planilha...", font=("Arial", 10),
            command=self.selecionar_arquivo, width=25,
        ).pack(pady=5)

        self.botao_gerar = tk.Button(
            janela, text="Gerar Relatório", font=("Arial", 11, "bold"),
            command=self.gerar_relatorio, width=25, height=2,
            bg="#2E5EAA", fg="white", state="disabled",
        )
        self.botao_gerar.pack(pady=15)

        self.rotulo_status = tk.Label(janela, text="", font=("Arial", 9), fg="#2E5EAA")
        self.rotulo_status.pack()

    def selecionar_arquivo(self):
        caminho = filedialog.askopenfilename(
            title="Selecione a planilha de vendas",
            filetypes=[("Planilhas Excel", "*.xlsx")],
        )
        if caminho:
            self.caminho_planilha = caminho
            self.rotulo_arquivo.config(text=os.path.basename(caminho), fg="#1D2433")
            self.botao_gerar.config(state="normal")

    def gerar_relatorio(self):
        if not self.caminho_planilha:
            return

        self.rotulo_status.config(text="Gerando relatório, aguarde...")
        self.janela.update_idletasks()

        try:
            resultado = executar_pipeline(self.caminho_planilha)
        except (FileNotFoundError, ValueError) as erro:
            self.rotulo_status.config(text="")
            messagebox.showerror("Erro ao gerar relatório", str(erro))
            return
        except Exception as erro:  # erro inesperado: melhor mostrar do que travar em silêncio
            self.rotulo_status.config(text="")
            messagebox.showerror("Erro inesperado", f"Algo deu errado:\n{erro}")
            return

        self.rotulo_status.config(text="Relatório gerado com sucesso!")

        resposta = messagebox.askyesno(
            "Relatório gerado",
            f"O relatório foi salvo em:\n{PASTA_SAIDA_PADRAO}\n\n"
            "Deseja abrir essa pasta agora?",
        )
        if resposta:
            self._abrir_pasta(str(PASTA_SAIDA_PADRAO))

    @staticmethod
    def _abrir_pasta(caminho_pasta: str):
        if sys.platform == "win32":
            os.startfile(caminho_pasta)
        elif sys.platform == "darwin":
            os.system(f'open "{caminho_pasta}"')
        else:
            os.system(f'xdg-open "{caminho_pasta}"')


if __name__ == "__main__":
    janela = tk.Tk()
    app = AppRelatorios(janela)
    janela.mainloop()
