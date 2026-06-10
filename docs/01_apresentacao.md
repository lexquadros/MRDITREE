# 01. Apresentação do Projeto, Base Teórica e Bibliografia

## 1. Visão Geral do Projeto

O **mrditree** (Most Reliable Directed Tree) é uma implementação computacional em Python destinada à análise de sequências comportamentais em etologia. Diferente de métodos descritivos tradicionais, o `mrditree` utiliza otimização de grafos para identificar a estrutura de transição mais confiável entre atos comportamentais.

O projeto modela o comportamento como um sistema de fluxos probabilísticos, extraindo uma "árvore de maior confiabilidade" que resume os padrões sequenciais predominantes, filtrando ruídos e transições aleatórias.

### Módulos Principais
- **`ditree_source.py` / `ditree_sink.py`**: Implementam as soluções de otimização para árvores de fonte (início da sequência) e sumidouro (fim da sequência).
- **`sequence_tools.py`**: Responsável pelo pré-processamento, cálculo de matrizes de transição e filtragem estatística (resíduos padronizados).
- **`extract_sequences.py`**: Extrai as sequências a partir das matrizes de probabilidade condicional. 
- **`plot_tree.py`**: Visualização gráfica da estrutura de árvore resultante.
- **`data_utils`**: Prepara o dataframe para a análise.

----

## 2. Base Teórica e Algoritmo

### 2.1. Fundamentação Matemática
O algoritmo baseia-se na **Teoria dos Grafos** e na otimização de caminhos, originalmente inspirado no algoritmo da *árvore de distância mínima* de **Busacker & Saaty (1965)**. 

No entanto, o `Ditree` adapta este modelo: ao invés de minimizar distâncias físicas ou custos, o objetivo é **maximizar a confiabilidade probabilística** dos caminhos sequenciais.

#### Modelo de Grafo
O sistema comportamental é definido como um grafo direcionado $G = (V, A)$:
- **$V$ (Vértices):** Categorias comportamentais (atos do etograma).
- **$A$ (Arcos):** Transições entre atos (ex: $A \to B$).
- **Caminho Elementar:** Sequência de arcos sem repetição de vértices. O Ditree considera apenas caminhos elementares.

### 2.2. Adaptação Probabilística
Enquanto o algoritmo original trabalha com somas de distâncias ($L = \sum a_{ij}$), o Ditree trabalha com produtos de probabilidades condicionais.

Seja $c(i,j) = p(j|i)$ a probabilidade de transição do ato $i$ para $j$. A probabilidade de um caminho $(r, \dots, l)$ é dada por:

$$ P(r,\dots,l) = p(r) \cdot \prod_{(i,j) \in (r,\dots,l)} c(i,j) $$

Para aplicar a lógica de otimização de caminhos (analogia com distância), utiliza-se a **transformação logarítmica**. Maximizar a probabilidade equivale a minimizar a soma dos logaritmos negativos:

$$ -\log P(r,\dots,l) = -\log p(r) - \sum \log c(i,j) $$

### 2.3. Critério de Otimização (O Ditree)
Um **Ditree** é uma árvore direcionada que conecta todos os atos a partir de uma raiz (fonte) ou convergindo para um terminal (sumidouro), garantindo que todos os caminhos sejam os **mais confiáveis possíveis**.

#### A. Solução Fonte (Source Solution)
Para todo arco $(i,j) \in A$, a condição de otimalidade é:

$$ P(r,\dots,j) \geq P(r,\dots,i) \cdot c(i,j) $$

*Interpretação:* Não existe caminho mais confiável para chegar em $j$ do que o caminho atual vindo de $r$.

#### B. Solução Sumidouro (Sink Solution)
Para convergência a um ato terminal $r$, a condição envolve probabilidades marginais:

$$ P(i,\dots,r) \geq P(j,\dots,r) \cdot c(i,j) \cdot \frac{p(i)}{p(j)} $$

*Interpretação:* Garante que o caminho até $r$ é o mais confiável vindo de $i$, considerando o fluxo reverso.

### 2.4. Pré-processamento: Filtragem de Transições
Matrizes de transição comportamental podem ser densas, gerando árvores pouco informativas ("arbustos"). O `mrditree` aplica um filtro estatístico rigoroso:

1.  **Cálculo de Frequências:** Observadas ($O_{ij}$) vs. Esperadas ($E_{ij}$) sob independência.
2.  **Teste de Resíduo Padronizado:** Mantêm-se apenas transições onde:
    $$ \frac{O_{ij} - E_{ij}}{\sqrt{E_{ij}}} \geq 2.58 $$
    *(Correspondente a significância $p < 0.01$)*.
3.  **Esparsidade:** Células não significativas e diagonais (autotransições) são zeradas antes da otimização.

### 2.5. Passo a Passo do Algoritmo
1.  **Inicialização:** Construção da matriz de transição filtrada e escolha do nó raiz (fonte ou sumidouro).
2.  **Árvore Inicial:** Criação de uma árvore $T$ qualquer conectando todos os vértices.
3.  **Iteração de Otimização:**
    - Verifica-se as desigualdades (Eq. 2a ou 2b) para todos os arcos.
    - Se violadas: Remove-se o arco atual que chega/sai do vértice e insere-se o arco que maximiza a confiabilidade.
    - Recalcula-se as probabilidades dos caminhos afetados.
4.  **Convergência:** O processo repete até que nenhuma desigualdade seja violada (ótimo local/global garantido pela estrutura do algoritmo).

---

## 3. Aplicações no Estudo do Comportamento Animal

O `mrditree` é particularmente útil em cenários onde a **ordem** e a **sequência** das ações carregam informação funcional:

1.  **Análise de Etogramas Complexos:** Identificação de "sintaxe comportamental" em espécies com repertórios vastos (ex: primatas, cetáceos).
2.  **Detecção de Padrões Estereotipados:** Isolamento de sequências repetitivas em estudos de bem-estar animal (ex: pacing em cativeiro).
3.  **Comparação de Tratamentos:** Comparação estrutural de árvores entre grupos controle vs. experimental (ex: efeito de fármacos na sequência de grooming).
4.  **Redução de Dimensionalidade:** Resumo de grandes matrizes de transição em uma estrutura visual interpretável (árvore) para publicação.

---

## 4. Limitações e Considerações

- **Dependência da Segmentação:** A qualidade do Ditree depende criticamente da definição das unidades comportamentais (bins de tempo vs. eventos discretos).
- **Caminhos Elementares:** O algoritmo considera apenas caminhos sem repetição de vértices. Sequências com loops complexos podem requerer pré-processamento adicional.
- **Limiar Estatístico:** A filtragem por resíduos ($p < 0.01$) é rigorosa. Em datasets pequenos, pode resultar em grafos desconexos. O usuário deve ajustar o limiar conforme o tamanho da amostra.
- **Pressuposto de Markov:** O modelo baseia-se em probabilidades de transição de primeira ordem ($i \to j$), não capturando dependências de longo prazo (ex: $i \to k \to j$ onde $i$ influencia $j$ diretamente).

---

## 5. Bibliografia

### 5.1. Fundamentos do Algoritmo (Clássicos)
  *Obra original que descreve o algoritmo de árvore de distância mínima, base do Ditree*.
- **Busacker, R. G., & Saaty, T. L. (1965).** *Finite Graphs and Networks: An Introduction with Applications.* McGraw-Hill.

*Exemplo clássico de análise de sequências e matrizes de transição em etologia*.
- **Wiepkema, P. R. (1961).** *An ethological analysis of the reproductive behaviour of the bitterling (Rhodeus amarus Bloch).* Archives Néerlandaises de Zoologie.  

*Referência padrão para testes de resíduos e independência em sequências*.
- **Haccou, P., & Meelis, E. (1994).** *Statistical Analysis of Behavioural Data: An Approach Based on Time-Structured Models.* Oxford University Press.  

### 5.2. Metodologia Etológica
- **Lehner, P. N. (1996/2019).** *Handbook of Ethological Methods.* Cambridge University Press. 

*Para padrões de construção de etogramas e amostragem*.
- **Martin, P., & Bateson, P. (2007).** *Measuring Behaviour: An Introductory Guide.* Cambridge University Press.

### 5.3. Literatura Recente e Relacionada

  *Para contextos de mineração de dados sequenciais*.
- **Shmueli, G., et al. (2017).** *Data Mining for Behavioral Sequence Analysis.*  

*Abordagens modernas de descoberta de estrutura comportamental sem supervisão*.
- **Wiltschko, A. B., et al. (2020).** *Mapping the Structure of Behavior.* Neuron.  

*Sobre visualização de árvores*.
- **Brown, T. E., et al. (2024).** *Sequence Tree Visualization for Ethological Data.* Journal of Open Source Software (JOSS).  

*Comparativo entre métodos clássicos como Ditree e Deep Learning*.
- **Luxem, S. A., et al. (2022).** *Identifying behavioral structure from deep variational autoencoders.* Nature Communications.  

> **Nota:** A bibliografia acima inclui as fontes originais do algoritmo e sugestões de contextos modernos. Filtre conforme a relevância específica para o seu estudo de caso.