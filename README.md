# Análise de Dados de Espectrometria por Impedância

Este projeto tem como objetivo desenvolver uma ferramenta computacional para organizar, processar e analisar dados experimentais de espectrometria por impedância, utilizando Python e técnicas de ciência de dados.

O sistema está sendo desenvolvido como parte de uma Iniciação Científica no Programa de Formação Interdisciplinar Superior (ProFIS) da Universidade Estadual de Campinas (UNICAMP), com foco na otimização do fluxo de processamento de dados de uma língua eletrônica impedimétrica.

A proposta busca reduzir etapas manuais, melhorar a organização dos dados experimentais e estabelecer uma base computacional para análises estatísticas e futuras aplicações de Machine Learning.

---

## Funcionalidades implementadas

- Leitura automática de arquivos `.csv`, incluindo diferentes formatos e delimitadores.
- Extração e organização das informações de amostras, sensores e repetições.
- Geração automatizada de datasets estruturados em Excel.
- Organização dos dados por sensores e frequências.
- Interface gráfica para seleção de arquivos utilizando Tkinter.
- Preparação e tratamento dos dados experimentais.
- Centralização e padronização das variáveis.
- Aplicação de PCA (Análise de Componentes Principais).
- Visualização interativa dos resultados do PCA utilizando Plotly.
- Identificação das classes das amostras e visualização de sua distribuição no espaço dos componentes principais.

---

## Estrutura do Projeto

```text
IC_2026/
│
├── Amostras_antes/        # Arquivos CSV brutos
├── dados_processados/     # Arquivos Excel gerados
│
├── banco_IC.py            # Processamento, tratamento e análise dos dados
├── interface_IC.py        # Interface gráfica (Tkinter)
│
└── README.md              # Documentação do projeto
```

---

## Pipeline de processamento

O fluxo de processamento foi desenvolvido para automatizar as etapas de organização e análise dos dados experimentais.

1. Leitura dos arquivos CSV.
2. Identificação automática dos delimitadores.
3. Extração das informações de amostras, sensores e repetições.
4. Organização dos valores de impedância por frequência.
5. Exportação dos dados estruturados para Excel.
6. Preparação, centralização e padronização dos dados.
7. Aplicação da Análise de Componentes Principais (PCA).
8. Geração de visualizações interativas para exploração dos resultados.

---

## Análise por Componentes Principais (PCA)

A ferramenta já conta com uma etapa de análise multivariada utilizando PCA, permitindo reduzir a dimensionalidade dos dados e investigar possíveis padrões de distribuição entre as classes de amostras.

A visualização interativa permite:

- Observar a distribuição das amostras nos componentes principais.
- Identificar as classes por cores.
- Consultar informações individuais de cada amostra.
- Alternar a exibição dos nomes das amostras.
- Visualizar a porcentagem de variância explicada por cada componente.

Em um dos conjuntos experimentais utilizados nos testes, foram processadas 28 amostras e 124 variáveis. Os dois primeiros componentes principais explicaram aproximadamente 88% da variância total dos dados.

*Esse resultado é referente a um conjunto específico de testes, não representando necessariamente todos os conjuntos experimentais.*

---

## Como executar

### 1. Instalar as dependências

```bash
pip install pandas numpy matplotlib scikit-learn plotly openpyxl
```

### 2. Executar a interface

```bash
python interface_IC.py
```

### 3. Fluxo de utilização

- Selecionar os arquivos CSV experimentais.
- Executar o processamento pela interface.
- Gerar automaticamente o arquivo Excel na pasta `dados_processados/`.
- Utilizar os dados organizados nas etapas de tratamento e análise.

---

## Próximas etapas

- Aprimoramento da interface gráfica.
- Avaliação da separação e distribuição das classes no PCA.
- Testes com novos conjuntos de dados experimentais.
- Implementação de métodos de classificação.
- Investigação de técnicas de Machine Learning para identificação e predição de amostras.
- Avaliação dos resultados obtidos e comparação entre diferentes abordagens.

---

## Objetivo da pesquisa

Desenvolver uma ferramenta computacional capaz de otimizar o fluxo de processamento de dados experimentais de uma língua eletrônica impedimétrica, reduzindo intervenções manuais e contribuindo para a organização, análise e interpretação dos resultados.

---

## Tecnologias utilizadas

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Plotly
- Tkinter
- OpenPyXL

---

## Contexto acadêmico

Projeto desenvolvido no âmbito de Iniciação Científica do Programa de Formação Interdisciplinar Superior (ProFIS), na Universidade Estadual de Campinas (UNICAMP).

**Área:** Física e Computação

**Tema:** Organização e processamento de dados e predição.

**Título da pesquisa:** Otimização do fluxo de dados em uma língua eletrônica impedimétrica.

---

## Licença

Projeto acadêmico destinado a fins educacionais e de pesquisa.
