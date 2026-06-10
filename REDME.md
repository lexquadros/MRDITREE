# MRDITree: Most Reliable Directed Trees

**MRDITree** é uma aplicação Python para análise de **sequências comportamentais** baseada em **árvores orientadas de maior confiabilidade** (*Most Reliable Directed Trees*), adaptada do algoritmo de *Busacker & Saaty (1965)* para grafos probabilísticos. O modelo combina **cadeias de Markov de primeira ordem**, **teoria de grafos** e **otimização de caminhos** para identificar os **caminhos mais prováveis** entre categorias comportamentais, exibindo-os em **árvores hierárquicas e visualmente interpretáveis**.
Esse algoritmo foi desenvolvido inicialmente pelo **Prof. Dr. Takechi Sato do Departamento de Psicologia Experimental da USP**. Em sequência, o **Prof. Dr. Carlos C. Alberts do Departamento de Ciências Biológicas da UNESP-Assis** aplicou o algoritmo no estudo de autolimpeza do gato doméstico, dando origem a um software, EthoSeq. 
EthoSeq é um software para Windows que roda o algoritmo desenvolvido pelo prof. Takechi. 
As sequências usadas como exemplo de aplicação são do meu doutorado e para ver mais sobre: docs/03_sequencias_aves.md

##  Visão Geral

- **Source Solution**: Encontra os caminhos mais confiáveis que **partem de uma categoria específica**.
- **Sink Solution**: Encontra os caminhos mais confiáveis que **convergem para uma categoria específica**.
- **Visualização hierárquica**: Exibe transições com **probabilidades condicionais**.
- **Extração de sequências**: Gera DataFrames com todas as sequências mais prováveis.

## O que **MRDITREE** faz?
- Recebe uma matriz com comportamentos, sendo cada coluna uma instância de análise (espécie, indivíduo, etc), gera uma matriz de probabilidade condicional para cada instância;
- A partir da matriz de probabilidade condicional, elimina as transições ao acaso e constrói sequências comportamentais mais prováveis; 
- As sequências mais prováveis são transformadas em árvores probabilísticas de origem (source) e sumidouro (sink). Sobre o modelo teórico deja em docs/01_apresentacao.md

## Aplicações
- Estudos do comportamento animal.

# **Atenção**
- O algoritmo roda sem interrupções se iniciado em **main.ipynb**;
- Se iniciado em **main.py**, a cada imagem gerada de árvore probabilística, é necessário um "OK" do usuário.

## Estrutura do algoritmo
mrditree/

```text
mmrditree/
├── __init__.py
├── main.ipynb
├── main.py 
├── README.md
├── requirements.txt
├── docs/
│   ├── 01_apresentacao.md
│   ├── 02_ferramentas_estatisticas.md
│   └── 03_sequencias_aves.md
├── ditree_resources/
│   ├── __init__.py
│   ├── ditree_source.py
│   ├── ditree_sink.py
│   ├── extract_sequences.py
│   ├── plot_tree.py
│   └── sequence_tools.py
├── sequencias_aves/
├── output/
└── utils/
    ├── __init__.py
    └── data_utils.py
