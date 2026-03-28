import banco_IC
from banco_IC import organizar_curvas
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
import os

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

def processar_dados():

   status.config(text="Carregando Excel...")
   janela.update()

   caminho = filedialog.askopenfilename(
        title="Selecione o arquivo Excel",
        filetypes=[("Excel files", "*.xlsx")]
    )

   if not caminho:
        status.config(text="Nenhum arquivo selecionado")
        return

   status.config(text="Carregando dados...")
   janela.update()

   df = banco_IC.carregar_dados_excel(caminho)

   status.config(text="Extraindo matriz...")
   janela.update()

   X = banco_IC.extrair_matriz(df)

   status.config(text="Tratando dados...")
   janela.update()

   sr = banco_IC.tratar_dados(X)

   status.config(text=f"Dados prontos para PCA ({len(sr)} amostras)")
   
   saida = filedialog.asksaveasfilename(
    defaultextension=".xlsx",
    filetypes=[("Excel files", "*.xlsx")],
    title="Salvar dados tratados como"
)

   if not saida:
      status.config(text="Salvamento cancelado")
      return

   df_tratado = df.copy()
   colunas_freq = [c for c in df.columns if c.startswith("f_")]
   df_tratado[colunas_freq] = sr
   df_tratado.to_excel(saida, index=False)

# interface
janela = tk.Tk()
janela.title("Processador de Curvas - IC")
janela.geometry("400x300")

label = tk.Label(janela, text="Análise de Espectrometria", font=("Arial", 14, "bold"))
label.pack(pady=20)

botao = tk.Button(janela, text="Selecionar Arquivos CSV", command=selecionar_arquivos,
font=("Arial", 10), bg="#4CAF50", fg="white", padx=10, pady=5)
botao.pack(pady=10)

status= tk.Label(janela, text="Aguardando ação...", font=("Arial", 9))
status.pack(pady=10)

botao_processar = tk.Button(
   janela,
   text="Processar Dados",
   command=processar_dados,
   bg="#2196F3",
   fg="white",
   padx=10,
   pady=5
)
botao_processar.pack(pady=10)

if __name__ == "__main__":
    janela.mainloop()