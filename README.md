# Análise de Dados de Espectrometria por Impedância

Este projeto tem como objetivo organizar, processar e analisar dados laboratoriais de espectrometria por impedância, utilizando Python e técnicas de ciência de dados.

O sistema foi desenvolvido como parte de uma Iniciação Científica na UNICAMP (PROFIS), com foco na estruturação de dados experimentais e aplicação futura de métodos de Machine Learning.

---

## Funcionalidades

* Leitura automática de arquivos `.csv`, incluindo diferentes formatos
* Tratamento e padronização dos dados
* Geração de dataset estruturado em Excel
* Visualização de curvas de impedância
* Interface gráfica para seleção de arquivos (Tkinter)
* Pipeline automatizado de processamento

---

## Estrutura do Projeto

```id="n92b3p"
IC_2026/
│
├── Amostras_antes/        # Arquivos CSV brutos
├── dados_processados/     # Arquivos Excel gerados
│
├── banco_IC.py            # Processamento e organização dos dados
├── interface_IC.py        # Interface gráfica (Tkinter)
│
└── README.md              # Documentação do projeto
```

---

## Como funciona

Cada arquivo CSV contém dados de impedância elétrica em diferentes frequências.

O sistema:

1. Lê os arquivos CSV
2. Detecta automaticamente o delimitador (`;` ou `,`)
3. Extrai informações relevantes:

   * Amostra
   * Sensor (IDE)
   * Repetição
4. Organiza os valores em colunas (`f_0`, `f_1`, ..., `f_n`)
5. Gera um dataset estruturado em Excel

---

## Como executar

### 1. Instalar dependências

```bash id="yr5o2p"
pip install pandas numpy matplotlib
```

---

### 2. Executar a interface

```bash id="rj0xg2"
python interface_IC.py
```

---

### 3. Fluxo de uso

* Selecionar os arquivos `.csv`
* O sistema irá:

  * Processar os dados
  * Gerar automaticamente um arquivo Excel em `dados_processados/`

---

## Visualização de Dados

O sistema permite visualizar curvas de impedância para análise exploratória dos dados, representando o comportamento elétrico das amostras em função da frequência.

---

## Próximos passos

* Aplicação de PCA (Análise de Componentes Principais)
* Implementação de modelos de Machine Learning para classificação
* Identificação automática de padrões em amostras
* Melhorias na interface gráfica
* Organização por categorias de amostras

---

## Objetivo da Pesquisa

Desenvolver uma ferramenta capaz de:

* Organizar dados laboratoriais de forma automatizada
* Reduzir ruídos e inconsistências
* Auxiliar na análise científica
* Permitir classificação e predição de amostras

---

## Tecnologias utilizadas

* Python
* Pandas
* NumPy
* Matplotlib
* Tkinter

---

## Autor

Mikael Wesley
Iniciação Científica – PROFIS / UNICAMP

---

## Licença

Este projeto é acadêmico e destinado a fins educacionais e de pesquisa.
