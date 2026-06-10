# Fundamentos Teóricos de Cadeias de Markov em Estudos Comportamentais

## 1. O Processo Estocástico como Modelo Etológico

Este documento descreve a fundamentação teórica para a modelagem de sequências comportamentais animais utilizando Cadeias de Markov de primeira ordem. A abordagem assume que a organização temporal do comportamento não é aleatória, nem estritamente determinística, mas sim **sequencialmente dependente** e regida por probabilidades de transição.

Formalmente, definimos a sequência comportamental como um processo estocástico de tempo discreto $\{X_t, t = 0, 1, 2, \dots\}$, onde cada variável aleatória $X_t$ assume valores em um espaço de estados finito $S$, correspondente ao etograma definido para a espécie estudada.

### A Propriedade de Markov
A premissa central do modelo é a **Propriedade de Markov** (ou *memorylessness*), que postula que a probabilidade do próximo estado depende exclusivamente do estado atual, sendo condicionalmente independente do histórico passado:

$$
P(X_{t+1} = j \mid X_t = i, X_{t-1}, \dots, X_0) = P(X_{t+1} = j \mid X_t = i) = p_{ij}
$$

**Interpretação Biológica:**
Ao adotar este modelo, hipotetiza-se que o **estado comportamental observável atual** contém toda a informação biologicamente relevante (nível fisiológico, contexto imediato, intenções) necessária para determinar a probabilidade do próximo comportamento.

----

## 2. A Matriz de Transição como Estrutura Comportamental

A dinâmica do sistema é governada pela **Matriz de Transição** $P$, uma matriz quadrada $N \times N$ (onde $N = |S|$). Cada elemento $p_{ij}$ representa a probabilidade condicional de transição do estado $i$ para o estado $j$ em um único passo de tempo.

$$
P = \begin{bmatrix}
p_{11} & p_{12} & \cdots & p_{1N} \\
p_{21} & p_{22} & \cdots & p_{2N} \\
\vdots & \vdots & \ddots & \vdots \\
p_{N1} & p_{N2} & \cdots & p_{NN}
\end{bmatrix}
$$

### Interpretação dos Parâmetros
*   **Diagonal Principal ($p_{ii}$):** Representa a **persistência** ou "inércia" comportamental. Valores elevados indicam que, uma vez iniciado, o comportamento tende a ser mantido por múltiplos intervalos de tempo (ex.: *bouts* prolongados de alimentação ou descanso).
*   **Elementos Off-diagonal ($p_{ij}, i \neq j$):** Representam a **propensão de mudança**. Revelam a estrutura sequencial preferencial do animal (ex.: após um evento de *Vigília*, qual a probabilidade imediata de *Fuga* vs. *Descanso*?).
*   **Zeros Estruturais vs. Amostrais:**
    *   *Zero Estrutural:* Transição biologicamente impossível sob as leis físicas ou etológicas da espécie.
    *   *Zero Amostral:* Transição possível, mas não observada durante o período de amostragem (requer cautela na inferência).

---

## 3. Suposições Críticas e Limitações Biológicas

A aplicação de Cadeias de Markov em biologia exige a validação rigorosa de suas suposições fundamentais:

### 3.1. Homogeneidade Temporal (Estacionariedade)
O modelo padrão assume que a matriz $P$ é constante ao longo do tempo ($p_{ij}(t) = p_{ij}$).
*   **Desafio Biológico:** Comportamentos são frequentemente modulados por ritmos circadianos, ciclos de maré, estações do ano ou mudanças ontogenéticas.
*   **Implicação:** Se a probabilidade de transição varia sistematicamente com o tempo (ex.: padrões diurnos vs. noturnos), o modelo homogêneo pode gerar estimativas viesadas.
*   **Abordagem:** Testar a homogeneidade dividindo os dados em blocos temporais ou utilizar Cadeias de Markov Não-Homogêneas.

### 3.2. A Propriedade de Markov (Ordem do Processo)
Assume-se que o passado distante é irrelevante (Memória de Primeira Ordem).
*   **Desafio Biológico:** Muitos comportamentos exibem dependência de longo prazo ou períodos refratários (ex.: um animal não se alimenta novamente até que um tempo mínimo tenha passado desde a última refeição, independentemente do comportamento intermediário).
*   **Abordagem:**
    1.  Utilizar **Cadeias de Ordem Superior** ($P(X_{t+1} \mid X_t, X_{t-1})$).
    2.  Redefinir o espaço de estados para incluir variáveis latentes ou duração (ex.: estados compostos como "Alimentando_<5min").

### 3.3. Discretização do Tempo
O comportamento é contínuo, mas o modelo exige discretização em intervalos de amostragem ($\Delta t$).
*   **Viés de Amostragem:** A escolha de $\Delta t$ influencia diretamente os valores de $P$. Intervalos muito longos mascaram transições rápidas; intervalos muito curtos inflam artificialmente a diagonal principal devido à autocorrelação técnica.

---

## 4. Métricas Derivadas de Interesse Ecológico

A partir da matriz $P$, extraem-se métricas quantitativas robustas para análise etológica:

### 4.1. Distribuição Estacionária ($\pi$)
Para cadeias ergódicas, existe um vetor único $\pi$ tal que $\pi P = \pi$.
*   **Significado:** Representa o **Orçamento de Tempo (Time Budget)** assintótico. $\pi_j$ estima a proporção de tempo que o animal passará no comportamento $j$ no longo prazo, independentemente do estado inicial.
*   **Aplicação:** Comparação de estratégias energéticas entre grupos, sexos ou habitats.

### 4.2. Tempo Médio de Recorrência ($m_{jj}$)
Definido como $m_{jj} = 1 / \pi_j$.
*   **Significado:** Número esperado de passos de tempo para que o sistema retorne ao estado $j$ após tê-lo deixado.
*   **Aplicação:** Estimativa da frequência de eventos raros ou críticos (ex.: comportamentos antipredatórios ou reprodutivos).

### 4.3. Entropia da Taxa de Transição
Medida da imprevisibilidade ou flexibilidade comportamental.
*   **Significado:** Ambientes estáveis podem resultar em cadeias de baixa entropia (comportamento estereotipado), enquanto ambientes dinâmicos podem exigir alta entropia (comportamento flexível).

---

## 5. Inferência Estatística e Validação do Modelo

A robustez das conclusões depende da validação estatística do ajuste do modelo aos dados observados.

### 5.1. Estimação dos Parâmetros
Utiliza-se o **Estimador de Máxima Verossimilhança (MLE)**:
$$
\hat{p}_{ij} = \frac{n_{ij}}{\sum_{k=1}^{N} n_{ik}}
$$
Onde $n_{ij}$ é a contagem observada de transições do estado $i$ para o estado $j$.

### 5.2. Testes de Adequação (Goodness-of-Fit)
É imperativo testar se a suposição markoviana é válida para o conjunto de dados:
1.  **Teste de Independência:** Verifica se a sequência possui estrutura sequencial significativa ou se os comportamentos ocorrem independentemente (hipótese nula de independência). Utiliza-se frequentemente o teste Qui-quadrado de sequencialidade.
2.  **Teste de Ordem:** Compara a verossimilhança de um modelo de primeira ordem contra modelos de ordem superior.
    *   Ferramentas: Teste de Razão de Verossimilhança (Likelihood Ratio Test) ou comparação de critérios de informação (**AIC** / **BIC**).

---

## 6. Síntese Metodológica

Para fins de reporte em publicações científicas, a metodologia pode ser descrita conforme abaixo:

> "A organização temporal do comportamento foi modelada através de Cadeias de Markov de primeira ordem em tempo discreto. Assumiu-se inicialmente que as transições entre os estados do etograma constituem um processo estocástico homogêneo. A matriz de transição foi estimada via Máxima Verossimilhança baseada nas frequências de transição observadas. A validade da suposição de Markov (primeira ordem) e a estacionariedade das transições foram avaliadas mediante testes de razão de verossimilhança e critérios de informação de Akaike (AIC). A distribuição estacionária derivada da matriz foi utilizada como estimativa do orçamento de tempo assintótico da população estudada."

---

### Referências Sugeridas para Aprofundamento
*   *Aspey, W. P. (1977). Wolf spider sociobiology:  I. Agonistic display and dominance-subordinance relations in adult male Schizocosa crassipes. Behaviour, 62, 103–137.* 
*   *Bakeman, J., & Dorsey, D. W. (1980). The analysis of behavioral transitions.*
* *Dawkins, R. (1976). Hierarchical organization:  a candidate principle for ethology. In: P. P. G. Bateson and R. A. Hinde (Editors), Growing Points in Ethology, Cambridge University Press, Cambridge, pp. 7–54.* 
*   *Gottman, J. M., & Roy, A. K. (1990). Sequential analysis: A guide for behavioral researchers.*
* *Hooff, J. A. R. A. M. van, (1982). Categories and sequences of behaviour:  methods of description and analysis. In: K. R. Scherer and P. Ekman (Editors), Handbook of Methods in Nonverbal Behaviour Research, Cambridge University Press, Cambridge, pp. 362–439.*
*   *MacDonald, I. L., & Zucchini, W. (1997). Hidden Markov and other models for discrete-valued time series.*

## 7. Método Estatístico para Teste de Hipótese:

O código utiliza o Standardized Residual (resíduo padronizado), que é amplamente aceito em análises de transição comportamental e é o método padrão recomendado para o Ditree (Aspey, 1977; van Hooff, 1982).

Comparação com outros métodos:

* **Pearson’s Chi-Squared**: é útil para teste global de associação, mas não serve para identificar células individuais, como requer o Ditree. Requer grandes amostras.
* **Wagner’s Chi-Squared**: é uma adaptação para dados dependentes (sequenciais), mas pouco estudado no contexto do Ditree. Não requer grandes amostras.
        O método usado é uma versão adaptada do qui-quadrado de Wagner, que considera a natureza serial das transições (sequenciais), ajustando a estatística para dependência temporal.
        Para mais detalhes veja em: ditree_resources/sequence_tools.py
* **Standardized Residual** é o mais equilibrado, mais simples, e mais adequado para o algoritmo Ditree, pois:
        
  * Opera célula por célula,
  * Identifica desvios positivos (O > E),
  * É estatisticamente robusto,
  * E é amplamente utilizado em estudos etológicos (como o de Dawkins, 1976).

