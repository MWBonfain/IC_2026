import numpy as np
import pandas as pd
import os
import re
import plotly.express as px
from sklearn.decomposition import PCA 
from sklearn.neighbors import KNeighborsClassifier
print("banco_IC carregado")

PASTA_DADOS = "Amostras_antes"
PASTA_SAIDA = "dados_processados"
ARQUIVO_SAIDA = "curvas_impedancia_organizadas.xlsx"

os.makedirs(PASTA_SAIDA, exist_ok=True)


def organizar_curvas(lista_arquivos=None, caminho_saida=None):   #jeito antigo


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

def organizar_curvas_horizontal(lista_arquivos=None, caminho_saida=None): #jeito novo

    dados = {}
    frequencias_ref = None

    if lista_arquivos is None:
        arquivos = [
            os.path.join(PASTA_DADOS, a)
            for a in os.listdir(PASTA_DADOS)
            if a.endswith(".csv")
        ]
    else:
        arquivos = lista_arquivos

    for caminho in arquivos:

        arquivo = os.path.basename(caminho)
        print(f"Lendo arquivo: {arquivo}")

        try:

            match = re.search(
                r"IDE(\d+).*_([A-Za-z]+)(\d+)",
                arquivo
            )

            if match:
                
                ide = int(match.group(1))
                amostra = match.group(2)
                repeticao = int(match.group(3))
            else:
                 match = re.search(
            r"([A-Za-z]+)_IDE-(\d+)",
            arquivo
        )

            if match:

                amostra = match.group(1)
                ide = int(match.group(2))
                repeticao = 1

            else:

                print(f"Ignorado: {arquivo}")
                continue



        except Exception as e:
            print(f"Erro nome {arquivo}: {e}")
            continue

        try:

            with open(caminho, "r", encoding="utf-8") as f:
                conteudo = f.readlines()

            frequencias = []
            impedancias = []

            for linha in conteudo[4:]:

                partes = linha.strip().split(";")

                if len(partes) < 11:
                    continue

                try:

                    freq = float(
                        partes[4].replace(",", ".")
                    )

                    imp = float(
                        partes[10].replace(",", ".")
                    )

                    frequencias.append(freq)
                    impedancias.append(imp)

                except:
                    continue

            if len(impedancias) == 0:
                continue

            if frequencias_ref is None:
                frequencias_ref = frequencias

            chave = f"{amostra}{repeticao}"

            if chave not in dados:
                dados[chave] = {}

            dados[chave][f"IDE{ide}"] = impedancias

            print(
                f"{arquivo} → {len(impedancias)} pontos"
            )

        except Exception as e:
            print(f"Erro CSV {arquivo}: {e}")

    linhas_excel = []

    for amostra in sorted(dados.keys()):

        linha = {}

        for ide in sorted(dados[amostra].keys()):

            curva = dados[amostra][ide]

            for freq, imp in zip(frequencias_ref, curva):

                linha[(ide, str(freq))] = imp

        linhas_excel.append(
            pd.Series(
                linha,
                name=amostra
            )
        )

    df = pd.DataFrame(linhas_excel)

    df.columns = pd.MultiIndex.from_tuples(df.columns)

    df.index.name = "ID"

    print("Shape final:", df.shape)

    if caminho_saida is None:
        caminho_saida = os.path.join(
            PASTA_SAIDA,
            "curvas_horizontal.xlsx"
        )

    print("SALVANDO EM:", caminho_saida)

    with pd.ExcelWriter(
        caminho_saida,
        engine="openpyxl"
    ) as writer:

        df.to_excel(writer)

    return df

def carregar_dados_excel(caminho):

    df = pd.read_excel(caminho, header=[0, 1])
    df = df.dropna(how="all")

    segunda_coluna = df.columns[1]

    df = df[
        df[segunda_coluna].astype(str) != "ID"
    ]

    df = df.reset_index(drop=True)

    print("Excel carregado")
    print(f"Total de amostras: {len(df)}")
    print(df.columns)
    print(df.iloc[:, 0])

    return df

def extrair_matriz(df):
    X = df.iloc[:, 2:]
    X = X.apply(pd.to_numeric, errors="coerce")
    X = X.fillna(0)

    X = X.values

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


    
def plot_pca(X_pca, df, classes=None):
    # Identificação das amostras na segunda coluna do Excel
    ids = df.iloc[:, 1].astype(str).to_numpy()

    if len(X_pca) != len(ids):
        raise ValueError(
            "A quantidade de amostras não corresponde "
            "à quantidade de pontos da PCA."
        )

    # Monta os dados das componentes principais
    dados_grafico = {
        "PC1": X_pca[:, 0],
        "PC2": X_pca[:, 1],
        "Amostra": ids
    }

    # Classes são opcionais; precisam representar os grupos reais
    if classes is not None:
        if len(classes) != len(X_pca):
            raise ValueError(
                "A quantidade de classes não corresponde "
                "à quantidade de amostras."
            )

        dados_grafico["Classe"] = classes

    fig = px.scatter(
        dados_grafico,
        x="PC1",
        y="PC2",
        color="Classe" if classes is not None else None,
        hover_name="Amostra",
        hover_data=["PC1", "PC2"],
        title="PCA - Análise das amostras",
        labels={
            "PC1": "Componente Principal 1",
            "PC2": "Componente Principal 2",
            "Classe": "Classe"
        }
    )

    fig.update_traces(
        marker=dict(size=11, line=dict(width=1, color="white"))
    )

    fig.update_layout(
        template="plotly_white",
        width=900,
        height=650,
        title_x=0.5,
        xaxis=dict(zeroline=True),
        yaxis=dict(zeroline=True)
    )

    fig.write_html(
    "grafico_pca.html",
    auto_open=True
)
