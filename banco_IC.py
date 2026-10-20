import numpy as np
import pandas as pd
import os
import re
import plotly.express as px
import plotly.graph_objects as go
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

def organizar_curvas_horizontal(lista_arquivos=None, caminho_saida=None):
    dados = {}
    frequencias_encontradas = set()

    if lista_arquivos is None:
        arquivos = [
            os.path.join(PASTA_DADOS, a)
            for a in os.listdir(PASTA_DADOS)
            if a.lower().endswith(".csv")
        ]
    else:
        arquivos = lista_arquivos

    for caminho in arquivos:
        arquivo = os.path.basename(caminho)
        print(f"Lendo arquivo: {arquivo}")

        # 1. Identifica amostra, sensor e repetição pelo nome
        nome_sem_extensao = os.path.splitext(arquivo)[0]

        match = re.match(
            r"^EC\d+_IDE(\d+)S\d+_(.+?)(\d+)$",
            nome_sem_extensao,
            re.IGNORECASE
        )

        if match:
            ide = int(match.group(1))
            amostra = match.group(2)
            repeticao_arquivo = int(match.group(3))

        else:
            # Compatibilidade com nomes antigos, como AGUA_IDE-1.csv
            match = re.match(
                r"^(.+?)_IDE-?(\d+)$",
                nome_sem_extensao,
                re.IGNORECASE
            )

            if match:
                amostra = match.group(1)
                ide = int(match.group(2))
                repeticao_arquivo = 1
            else:
                print(
                    f"Ignorado: formato de nome não reconhecido: "
                    f"{arquivo}"
                )
                continue

        # 2. Lê os dados do Solatron
        try:
            with open(caminho, "r", encoding="utf-8-sig") as f:
                conteudo = f.readlines()

            curvas_sweeps = {}

            # O cabeçalho do Solatron ocupa as primeiras quatro linhas.
            for linha in conteudo[4:]:
                partes = linha.strip().split(";")

                if len(partes) < 11:
                    continue

                try:
                    sweep = int(partes[1].strip())
                    freq = float(
                        partes[4].strip().replace(",", ".")
                    )
                    imp = float(
                        partes[10].strip().replace(",", ".")
                    )

                    if not (
                        np.isfinite(freq)
                        and np.isfinite(imp)
                    ):
                        continue

                    # Evita pequenas diferenças de representação
                    # numérica na mesma frequência.
                    freq = float(f"{freq:.7g}")

                    if sweep not in curvas_sweeps:
                        curvas_sweeps[sweep] = {}

                    curvas_sweeps[sweep][freq] = imp
                    frequencias_encontradas.add(freq)

                except (ValueError, IndexError):
                    continue

            if not curvas_sweeps:
                print(
                    f"Nenhuma medida válida encontrada em {arquivo}"
                )
                continue

            # 3. Cada sweep vira uma repetição independente
            nome_sensor = f"IDE{ide}"

            for sweep, curva in curvas_sweeps.items():
                chave = (
                    f"{amostra}{repeticao_arquivo}_R{sweep}"
                )

                if chave not in dados:
                    dados[chave] = {}

                if nome_sensor in dados[chave]:
                    print(
                        f"Aviso: {nome_sensor} duplicado para "
                        f"{chave}. Arquivo: {arquivo}"
                    )
                    continue

                dados[chave][nome_sensor] = curva

                print(
                    f"{arquivo} → amostra: {amostra}, "
                    f"sensor: {nome_sensor}, "
                    f"repetição do arquivo: {repeticao_arquivo}, "
                    f"sweep: {sweep}, "
                    f"pontos: {len(curva)}"
                )

        except Exception as e:
            print(f"Erro CSV {arquivo}: {e}")
            continue

    # 4. Confere se os dados foram carregados
    if not dados or not frequencias_encontradas:
        raise ValueError(
            "Nenhuma curva foi carregada. Confira os nomes dos "
            "arquivos e as colunas de frequência e impedância."
        )

    # Frequências em ordem decrescente: 1 MHz até 1 Hz
    frequencias_ref = sorted(
        frequencias_encontradas,
        reverse=True
    )

    # 5. Monta a tabela horizontal
    linhas_excel = []

    for amostra_id in sorted(dados.keys()):
        linha = {}

        sensores = sorted(
            dados[amostra_id].keys(),
            key=lambda nome: int(nome.replace("IDE", ""))
        )

        for sensor in sensores:
            curva = dados[amostra_id][sensor]

            for freq in frequencias_ref:
                # Se uma medida realmente não existir, deixa NaN.
                # Não inventa impedância igual a zero.
                linha[(sensor, str(freq))] = curva.get(
                    freq, np.nan
                )

        linhas_excel.append(
            pd.Series(linha, name=amostra_id)
        )

    df = pd.DataFrame(linhas_excel)

    if df.empty or len(df.columns) == 0:
        raise ValueError(
            "A tabela ficou vazia após a organização das curvas."
        )

    df.columns = pd.MultiIndex.from_tuples(df.columns)
    df.index.name = "ID"

    print("Shape final:", df.shape)
    print("Número de frequências:", len(frequencias_ref))
    print("Maior frequência:", max(frequencias_ref))
    print("Menor frequência:", min(frequencias_ref))

    # 6. Define o caminho de saída
    if caminho_saida is None:
        caminho_saida = os.path.join(
            PASTA_SAIDA,
            "curvas_horizontal.xlsx"
        )

    pasta_destino = os.path.dirname(caminho_saida)

    if pasta_destino:
        os.makedirs(pasta_destino, exist_ok=True)

    print("SALVANDO EM:", caminho_saida)

    # 7. Exporta para Excel
    with pd.ExcelWriter(
        caminho_saida,
        engine="openpyxl"
    ) as writer:
        df.to_excel(writer)

    print("Arquivo Excel salvo com sucesso!")

    return df

def carregar_dados_excel(caminho):
    df = pd.read_excel(caminho, header=[0, 1], index_col=0)

    # Remove linhas e colunas completamente vazias
    df = df.dropna(how="all", axis=0)
    df = df.dropna(how="all", axis=1)

    # Garante que os valores do corpo sejam numéricos
    df = df.apply(pd.to_numeric, errors="coerce")

    print("Excel carregado")
    print("Total de amostras:", len(df))
    print("Total de colunas:", len(df.columns))
    print("Primeiras colunas:", list(df.columns[:5]))
    print("Primeira frequência:", df.columns[0])

    return df

def extrair_matriz(df):
    X_df = df.copy()

    X_df = X_df.apply(pd.to_numeric, errors="coerce")

    # Mostra exatamente onde estão os valores ausentes
    faltantes = X_df.isna().sum().sum()

    print("Matriz extraída")
    print("Shape:", X_df.shape)
    print("Valores ausentes:", int(faltantes))
    print("Primeiras colunas:", list(X_df.columns[:5]))

    if faltantes > 0:
        colunas_com_faltantes = X_df.columns[
            X_df.isna().any()
        ].tolist()

        print("Colunas com valores ausentes:", colunas_com_faltantes)

        raise ValueError(
            f"Foram encontrados {int(faltantes)} valores ausentes. "
            "Confira as colunas listadas no terminal."
        )

    return X_df.to_numpy(dtype=float)

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
    

def plot_pca(X_pca, df, pca=None):
    # Confere se existem pelo menos dois componentes principais
    if X_pca.shape[1] < 2:
        raise ValueError(
            "O PCA precisa ter pelo menos dois componentes "
            "para gerar este gráfico."
        )

    # Recupera os nomes originais das amostras do índice
    amostras = df.index.astype(str).tolist()

    # Garante que o número de identificadores corresponda aos pontos
    if len(amostras) != len(X_pca):
        raise ValueError(
            "O número de amostras não corresponde ao número "
            "de pontos gerados pelo PCA."
        )

    # Identifica a classe a partir do nome da amostra
    def identificar_classe(nome):
        # Remove a identificação da repetição da curva, como _R1
        nome_base = re.sub(r"_R\d+$", "", nome, flags=re.IGNORECASE)

        classe = re.sub(r"\d+$", "", nome_base).strip(" _-")

        return classe if classe else nome_base

    classes = [identificar_classe(nome) for nome in amostras]

    dados_grafico = pd.DataFrame({
        "PC1": X_pca[:, 0],
        "PC2": X_pca[:, 1],
        "Amostra": amostras,
        "Classe": classes
    })

    if pca is not None:
        variancia_pc1 = pca.explained_variance_ratio_[0] * 100
        variancia_pc2 = pca.explained_variance_ratio_[1] * 100

        eixo_x = f"PC1 ({variancia_pc1:.2f}%)"
        eixo_y = f"PC2 ({variancia_pc2:.2f}%)"
    else:
        eixo_x = "PC1"
        eixo_y = "PC2"


    fig = px.scatter(
        dados_grafico,
        x="PC1",
        y="PC2",
        color="Classe",
        text="Amostra",
        hover_name="Amostra",
        hover_data={
            "Classe": True,
            "PC1": ":.4f",
            "PC2": ":.4f"
        },
        color_discrete_sequence=px.colors.qualitative.Set2,
        labels={
            "PC1": eixo_x,
            "PC2": eixo_y,
            "Classe": "Classe da amostra"
        },
        title="PCA — Análise de Componentes Principais"
    )


    fig.update_traces(
        textposition="top center",
        marker=dict(size=11, opacity=0.85),
        textfont=dict(size=10)
    )

    fig.update_layout(
        template="plotly_white",
        legend_title_text="Classe",
        hovermode="closest",
        font=dict(family="Arial", size=13),
        title_x=0.5,
        xaxis=dict(
            zeroline=True,
            showgrid=True
        ),
        yaxis=dict(
            zeroline=True,
            showgrid=True
        )
    )

    fig.show()
    return fig
