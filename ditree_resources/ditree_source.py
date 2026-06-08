import numpy as np
from ditree_resources.sequence_tools import conditional_prob_matrix, significant_transitions_sd

# Ditree source -> sink
def ditree_source(observed_transitions, acts, source, alpha=0.01):
    """
    Algoritmo DITree - Source Solution.
    Encontra a árvore direcionada mais confiável com raiz em 'source'.

    Retorna:
        - parent: dict indicando o pai de cada nó na árvore final.
        - path_probs: probabilidade de cada caminho da fonte até os nós.
    """
    n = len(acts)
    act_to_idx = {act: i for i, act in enumerate(acts)}
    idx_to_act = {i: act for act, i in act_to_idx.items()}

    source_idx = act_to_idx[source]

    # Matriz de probabilidades condicionais
    cond_prob = conditional_prob_matrix(observed_transitions)

    # Esperado sob independência (modelo log-linear de independência)
    total_transitions = observed_transitions.sum()
    row_totals = observed_transitions.sum(axis=1)
    col_totals = observed_transitions.sum(axis=0)
    expected = np.outer(row_totals, col_totals) / total_transitions

    # Zerar transições não significativas
    mask = significant_transitions_sd(observed_transitions, expected, alpha=alpha)
    filtered_cond_prob = cond_prob.copy()
    filtered_cond_prob[~mask] = 0.0

    # Inicializar árvore: inicialmente, todos os nós apontam para source (exceto source)
    parent = {i: None for i in range(n)}
    parent[source_idx] = -1  # Raiz

    # Inicializa caminhos: cada nó conectado diretamente à fonte, se possível
    for j in range(n):
        if j != source_idx and filtered_cond_prob[source_idx, j] > 0:
            parent[j] = source_idx

    # Probabilidade dos caminhos (P(r,...,k))
    path_probs = np.zeros(n)
    path_probs[source_idx] = 1.0  # P(r) = 1 (relativa)

    # Atualiza caminhos iniciais
    for j in range(n):
        if parent[j] is not None and parent[j] != -1:
            path_probs[j] = filtered_cond_prob[source_idx, j]

    # Algoritmo iterativo
    improved = True
    while improved:
        improved = False

        for i in range(n):  # ato i
            for j in range(n):  # ato j
                if i == j or filtered_cond_prob[i, j] == 0:
                    continue

                # Verifica se P(r->j) >= P(r->i) * P(j|i)
                if path_probs[j] < path_probs[i] * filtered_cond_prob[i, j]:
                    # Violação encontrada: atualizar caminho para j via i
                    if parent[j] is not None and parent[j] != -1:
                        # Remove arco atual que termina em j
                        old_parent = parent[j]
                        # Não precisamos fazer nada além de reatribuir
                    parent[j] = i
                    path_probs[j] = path_probs[i] * filtered_cond_prob[i, j]
                    improved = True

        # Após cada iteração, garante que não há ciclos (não implementado aqui, mas garantido por construção)

    # Converter para nomes
    parent_names = {idx_to_act[i]: (idx_to_act[parent[i]] if parent[i] is not None and parent[i] != -1 else None)
                    for i in range(n) if parent[i] is not None}
    path_probs_dict = {idx_to_act[i]: path_probs[i] for i in range(n)}

    return parent_names, path_probs_dict, filtered_cond_prob
