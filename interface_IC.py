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

def aplicar_pca_interface():
   status.config(text="Selecionando Excel tratado... ")
   janela.update()

   arquivos = filedialog.askopenfilenames(
        title="Selecione o(s) Excel(s) tratado(s)",
        filetypes=[("Excel files", "*.xlsx")]
    )

   if not arquivos:
        return

   status.config(text="Processando PCA...")
   janela.update()

   for caminho in arquivos:

        df = banco_IC.carregar_dados_excel(caminho)
        X = banco_IC.extrair_matriz(df)
        sr = banco_IC.tratar_dados(X)

        X_pca, pca = banco_IC.aplicar_pca(sr)

        banco_IC.plot_pca(X_pca, df)

   status.config(text="PCA finalizado!")

# interface
janela = tk.Tk()
janela.title("Processador de Curvas - IC")
janela.geometry("600x400")
janela.configure(bg="#1e1e2f")

frame = tk.Frame(janela,bg="#1e1e2f")
frame.pack(pady=30)

titulo = tk.Label(
   frame,
   text="Análise de Espectrometria", 
   font=("Arial", 14, "bold"),
   bg="#1e1e2f",
   fg="white"
)
titulo.pack(pady=20)

botao_csv = tk.Button(
   frame,
   text="Selecionar Arquivos CSV", 
   command=selecionar_arquivos,
   font=("Arial", 10, "bold"),
   relief="flat",
   bg="#4CAF50", 
   fg="white", 
   padx=10, 
   pady=8
)
botao_csv.pack(pady=8, padx=40, fill='x')

botao_processar = tk.Button(
   frame,
   text="Processar Dados",
   command=processar_dados,
   bg="#2196F3",
   fg="white",
   font=("Arial", 10, "bold"),
   relief="flat",
   padx=10,
   pady=8
)
botao_processar.pack(pady=8, padx=50, fill='x')

botao_pca = tk.Button(
    frame,
    text="Aplicar PCA",
    command=aplicar_pca_interface,
    bg="#9C27B0",
    fg="white",
    font=("Arial", 10, "bold"),
    relief="flat",
    padx=10,
    pady=8
)
botao_pca.pack(fill="x",padx=40, pady=8 )

status = tk.Label(
    frame,
    text="Aguardando ação...",
    font=("Arial", 9),
    bg="#1e1e2f",
    fg="#cccccc"
)
status.pack(pady=15)


if __name__ == "__main__":
    janela.mainloop()