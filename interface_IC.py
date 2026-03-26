from banco_IC import organizar_curvas
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np

def selecionar_arquivos():

    status.config(text="Selecionando arquivos...")
    janela.update()

    arquivos = filedialog.askopenfilenames(
        title="Selecione os CSVs",
        filetypes=[("CSV files", "*.csv")]
    )

    if arquivos:

      status.config(text="Processando dados...")
      janela.update()


      caminho_saida=filedialog.asksaveasfilename(
         defaultextension="xlsx",
         filetypes=[("Excel files", "*xlsx")],
         title = "Salvar arquivo como"
      )

      if not caminho_saida:
         return
      
      df = organizar_curvas(
         lista_arquivos=arquivos,
         caminho_saida=caminho_saida
      )


      messagebox.showinfo(
            "Sucesso",
            f"{len(df)} curvas processadas!"
        )


# interface
janela = tk.Tk()
janela.title("Processador de Curvas - IC")
janela.geometry("400x300")

label = tk.Label(janela, text="Análise de Espectometria", font=("Arial", 14, "bold"))
label.pack(pady=20)

botao = tk.Button(janela, text="Selecionar Arquivos CSV", command=selecionar_arquivos,
font=("Arial", 10), bg="#4CAF50", fg="white", padx=10, pady=5)
botao.pack(pady=10)

status= tk.Label(janela, text="Aguardando ação...", font=("Arial", 9))
status.pack(pady=10)

if __name__ == "__main__":
    janela.mainloop()