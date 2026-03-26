import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

print("banco_IC carregado")

PASTA_DADOS = "Amostras_antes"
PASTA_SAIDA = "dados_processados"
ARQUIVO_SAIDA = "curvas_impedancia_organizadas.xlsx"

os.makedirs(PASTA_SAIDA, exist_ok=True)


def organizar_curvas(lista_arquivos=None, caminho_saida=None):


    registros = []

    if lista_arquivos is None:
        arquivos = [os.path.join(PASTA_DADOS, a) for a in os.listdir(PASTA_DADOS) if a.endswith(".csv")]
    else:
        arquivos = lista_arquivos

    for caminho in arquivos:

        arquivo = os.path.basename(caminho)
        print(f"Lendo arquivo: {arquivo}")

        with open(caminho, "r", encoding="utf-8") as f:

            for linha in f:

                linha = linha.strip()

                if not linha:
                    continue

                # aceita ; ou ,
                import re
                partes = re.split(r"[;,]", linha)

                if len(partes) < 2:
                    continue

                identificador = partes[0].strip()

                if identificador == "":
                    continue

                valores = []
                for v in partes[1:]:
                    try:
                        valores.append(float(v))
                    except:
                        valores.append(np.nan)

                try:
                    if "_IDE_" in identificador:
                        amostra, ide_rep = identificador.split("_IDE_")
                        ide, repeticao = ide_rep.split("-")
                    else:
                        partes_id = identificador.split(" ")
                        amostra = partes_id[0]
                        repeticao = partes_id[1] if len(partes_id) > 1 else 0
                        ide = "1"

                except:
                    print(f"Ignorado: {identificador}")
                    continue

                registro = {
                    "amostra": amostra,
                    "sensor": f"IDE_{ide}",
                    "repeticao": int(repeticao)
                }

                for i, val in enumerate(valores):
                    registro[f"f_{i}"] = val

                registros.append(registro)

    df = pd.DataFrame(registros)

    if not df.empty:
        colunas_freq = [c for c in df.columns if c.startswith("f_")]
        df[colunas_freq] = df[colunas_freq].apply(pd.to_numeric, errors="coerce")

    if caminho_saida is None:
        caminho_saida = os.path.join(PASTA_SAIDA, ARQUIVO_SAIDA)

    print("SALVANDO EM:", caminho_saida)

    df.to_excel(caminho_saida, index=False)

    return df


# VISUALIZAÇÃO DE CURVAS

def plot_exemplo(df):

    primeira = df.iloc[0]

    valores = primeira.iloc[3:].values

    frequencias = np.logspace(0, 6, len(valores))

    plt.figure(figsize=(8,5))

    plt.plot(frequencias, valores)

    plt.xscale("log")

    plt.xlabel("Frequência (Hz)")
    plt.ylabel("Impedância (Ω)")
    plt.title(f"Curva exemplo – {primeira['amostra']}")

    plt.grid(True)

    plt.show()

if __name__ == "__main__":
    df = organizar_curvas()
    plot_exemplo(df)