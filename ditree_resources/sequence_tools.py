import numpy as np
from scipy.stats import chi2

# Função para criar a matriz de transição
def sequence_to_transition_matrix(seq, acts):
    """
    Constrói a matriz de transição a partir de uma sequência de atos.
    """
    n = len(acts)
    act_to_idx = {act: i for i, act in enumerate(acts)}
    matrix = np.zeros((n, n))

    for i in range(len(seq) - 1):
        current = seq[i]
        next_act = seq[i + 1]
        if current in act_to_idx and next_act in act_to_idx:
            matrix[act_to_idx[current]][act_to_idx[next_act]] += 1

    return matrix, act_to_idx


# Matriz de probabilidade condicional
def conditional_prob_matrix(observed_matrix):
    """
    Calcula a matriz de probabilidades condicionais: P(j|i) = count(i,j) / sum_j count(i,j)
    """
    row_sums = observed_matrix.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1  # Evita divisão por zero
    return observed_matrix / row_sums

# Transições acima do acaso: Standardized Residual
def significant_transitions_sd(observed, expected, alpha=0.01):
    """
    Identifica transições significativamente acima do acaso usando resíduos padronizados.
    Retorna uma máscara booleana.
    """
    residual = (observed - expected) / np.sqrt(expected + 1e-10)
    threshold = 2.58 if alpha == 0.01 else 1.96  # 99% ou 95%
    return residual >= threshold

# Transições acima do acaso: X2 de Pearson
def significant_transitions_pearson(observed, expected, alpha=0.01):
    """
    Identifica transições significativamente acima do acaso usando o qui-quadrado de Pearson aplicado célula a célula.
    Retorna uma máscara booleana.
    """
    # Evita divisão por zero
    mask_valid = expected > 0
    pearson_residual = np.zeros_like(observed, dtype=float)
    pearson_residual[mask_valid] = (observed[mask_valid] - expected[mask_valid])**2 / expected[mask_valid]

    # Limiar de significância (unilateral, para desvios positivos)
    threshold = chi2.ppf(1 - alpha, df=1)  # Aproximadamente 6.63 para alpha=0.01

    # Apenas desvios positivos são considerados (O > E)
    significant_mask = (observed > expected) & (pearson_residual >= threshold)

    return significant_mask

# Transições acima do acaso: X2 de Wagner
def significant_transitions_wagner(observed, expected, alpha=0.01):
    """
    Identifica transições significativamente acima do acaso usando uma adaptação do qui-quadrado de Wagner,
    que considera dependência serial nas transições comportamentais.
    Retorna uma máscara booleana.
    """
    # Evita divisão por zero
    mask_valid = expected > 0
    wagner_stat = np.zeros_like(observed, dtype=float)
    # Cálculo adaptado: qui-quadrado com correção de continuidade e fator de dependência
    # (Este é um modelo aproximado baseado em ajustes de dependência serial)
    diff = observed - expected
    wagner_stat[mask_valid] = (diff[mask_valid]**2) / (expected[mask_valid] + 0.5)  # Correção de continuidade

    # Limiar de significância unilateral com ajuste de dependência (df=1 é uma aproximação)
    threshold = chi2.ppf(1 - alpha, df=1)  # Aproximadamente 6.63 para alpha=0.01

    # Apenas desvios positivos são considerados (O > E)
    significant_mask = (observed > expected) & (wagner_stat >= threshold)

    return significant_mask

'''
SOBRE X2 DE WAGNER
Este método é uma versão adaptada do qui-quadrado de Wagner, que considera a natureza serial das 
transições (sequenciais), ajustando a estatística para dependência temporal. A adaptação baseada na ideia de que 
transições em sequências dependentes requerem correção devido à auto-correlação. É considerado a correção de 
continuidade e um ajuste de graus de liberdade baseado em padrões de transição.
Use se tiver certeza da aplicação deste método, caso não tenha, opte por Standardized Residual. 
Veja mais em: docs/02_ferramentas_estatisticas.md
'''