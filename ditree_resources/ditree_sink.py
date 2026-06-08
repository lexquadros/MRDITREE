import numpy as np
from ditree_resources.sequence_tools import conditional_prob_matrix, significant_transitions_sd

def marginal_probabilities(seq, acts):
    """
    Calcula p(i) = frequência relativa do ato i na sequência.
    """
    counts = {act: 0 for act in acts}
    for act in seq:
        if act in counts:
            counts[act] += 1
    total = len(seq)
    return np.array([counts[act] / total for act in acts])

def ditree_sink(observed_transitions, acts, seq, sink, alpha=0.01):
    """
    Algoritmo DITree - Sink Solution.
    Encontra a árvore direcionada mais confiável que converge para 'sink'.

    Retorna:
        - parent: dict indicando o pai de cada nó na árvore final (em direção ao sink).
        - path_probs: probabilidade de cada caminho dos nós até o sink.
    """
    n = len(acts)
    act_to_idx = {act: i for i, act in enumerate(acts)}
    idx_to_act = {i: act for act, i in act_to_idx.items()}

    sink_idx = act_to_idx[sink]

    # Matriz de probabilidades condicionais
    cond_prob = conditional_prob_matrix(observed_transitions)

    # Probabilidades marginais p(i)
    marginals = marginal_probabilities(seq, acts)

    # Esperado sob independência
    total_transitions = observed_transitions.sum()
    row_totals = observed_transitions.sum(axis=1)
    col_totals = observed_transitions.sum(axis=0)
    expected = np.outer(row_totals, col_totals) / total_transitions

    # Zerar transições não significativas
    mask = significant_transitions_sd(observed_transitions, expected, alpha=alpha)
    filtered_cond_prob = cond_prob.copy()
    filtered_cond_prob[~mask] = 0.0

    # Inicializar árvore convergente ao sink
    parent = {i: None for i in range(n)}
    parent[sink_idx] = -1  # Marca como sumidouro

    # Inicializar caminhos: cada nó conectado diretamente ao sink
    path_probs = np.zeros(n)
    path_probs[sink_idx] = 1.0  # Caminho do sink até ele mesmo

    for i in range(n):
        if i != sink_idx and filtered_cond_prob[i, sink_idx] > 0:
            parent[i] = sink_idx
            # P(i -> sink)
            path_probs[i] = filtered_cond_prob[i, sink_idx]

    # Algoritmo iterativo
    improved = True
    while improved:
        improved = False

        for i in range(n):  # nó i
            for j in range(n):  # nó j
                if i == j or filtered_cond_prob[i, j] == 0:
                    continue

                # Verifica condição de otimalidade (Equação 2b):
                # P(i->r) >= P(j->r) * P(i->j) * [p(i)/p(j)]
                # Ou seja, P(i->r) < P(j->r) * P(i->j) * [p(i)/p(j)] -> violação

                if marginals[j] == 0:
                    continue  # Evita divisão por zero

                prob_via_j = path_probs[j] * filtered_cond_prob[i, j] * (marginals[i] / marginals[j])

                if path_probs[i] < prob_via_j:
                    # Violação encontrada: atualizar caminho de i via j até r
                    parent[i] = j
                    path_probs[i] = prob_via_j
                    improved = True

    # Converter para nomes
    parent_names = {
        idx_to_act[i]: (idx_to_act[parent[i]] if parent[i] is not None and parent[i] != -1 else None)
        for i in range(n)
    }
    path_probs_dict = {idx_to_act[i]: path_probs[i] for i in range(n)}

    return parent_names, path_probs_dict, filtered_cond_prob
