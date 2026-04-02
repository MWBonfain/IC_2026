import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.decomposition import PCA 
from sklearn.neighbors import KNeighborsClassifier
from matplotlib.colors import ListedColormap
from matplotlib.widgets import CheckButtons 

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

def carregar_dados_excel(caminho):

    df = pd.read_excel(caminho)

    print("Excel carregado")
    print(f"Total de amostras: {len(df)}")

    return df

def extrair_matriz(df):
    colunas_freq = [c for c in df.columns if c.startswith("f_")]

    X = df[colunas_freq].values

    print("Matriz extraída")
    print("Shape:", X.shape)

    return X

def tratar_dados(X):

    media = np.mean(X, axis=0)
    centerx = X  - media
    stdr = np.std(centerx, axis=0, ddof=1)
    stdr[stdr == 0] = 1
    sr = centerx / stdr

    print("Dados tratados")
    
    return sr



def aplicar_pca(X, n_componentes=2):
    pca = PCA(n_components=n_componentes)

    X_pca = pca.fit_transform(X)

    print("\nPCA aplicado!")
    print("Variância aplicada:", pca.explained_variance_ratio_)
    return X_pca, pca

def plot_pca(X_pca, df):

    labels = df["amostra"].values
    classes = np.unique(labels)

    
    colors = [
        "#9C27B0",
        "#2196F3",
        "#4CAF50",
        "#FF9800",
        "#E91E63",
        "#00BCD4"
    ]

    # mapear classes → números
    label_map = {classe: i for i, classe in enumerate(classes)}
    y = np.array([label_map[l] for l in labels])

    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X_pca, y)

    x_min, x_max = X_pca[:, 0].min() - 1, X_pca[:, 0].max() + 1
    y_min, y_max = X_pca[:, 1].min() - 1, X_pca[:, 1].max() + 1

    xx, yy = np.meshgrid(
        np.linspace(x_min, x_max, 200),
        np.linspace(y_min, y_max, 200)
    )

    Z = knn.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.figure(figsize=(7,6))

    cmap_fundo = ListedColormap(colors[:len(classes)])
    fundo = plt.contourf(xx, yy, Z, alpha=0.15, cmap=cmap_fundo)
    

    for i, classe in enumerate(classes):

        idx = labels == classe

        plt.scatter(
            X_pca[idx, 0],
            X_pca[idx, 1],
            color=colors[i],
            label=classe,
            edgecolors="white",
            s=60
        )

    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title("PCA - Tratamento com dados")

    plt.legend()
    plt.grid(True)

    rax = plt.axes([0.75, 0.4, 0.2, 0.15]) 
    check = CheckButtons(rax, ["Regiões"], [True])

    def toggle(label):
        visivel = fundo.get_visible()
        fundo.set_visible(not visivel)
        plt.draw()

    check.on_clicked(toggle)

    plt.tight_layout()
    plt.show()
    plt.close()