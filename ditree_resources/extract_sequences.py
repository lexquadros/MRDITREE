import pandas as pd
import networkx as nx

def extract_sequences_from_ditree(parent_dict, path_probs_dict, acts):
    """
    Extrai todas as sequências completas (da raiz às folhas) a partir do parent_dict.

    Parâmetros:
    - parent_dict: dict no formato {child: parent} (None para a raiz)
    - path_probs_dict: dict {act: probabilidade_do_caminho_desde_a_raiz}
    - acts: lista completa de atos

    Retorna:
    - Lista de dicionários com: sequence, length, probability
    """
    # Reconstruir o grafo como um DiGraph
    G = nx.DiGraph()
    root = None
    for child, parent in parent_dict.items():
        if parent is None:
            root = child
        else:
            G.add_edge(parent, child)

    #if root is None:
        #return []
    if root is not None:
        G.add_node(root)

    # Encontrar todos os caminhos da raiz até as folhas (nós sem filhos)
    sequences = []
    leaf_nodes = [n for n in G.nodes if G.out_degree(n) == 0]  # Folhas
    if not leaf_nodes:
        leaf_nodes = [root]  # Caso degenerado

    for leaf in leaf_nodes:
        try:
            # Caminho da raiz até a folha
            path = nx.shortest_path(G, source=root, target=leaf)
            prob = path_probs_dict.get(leaf, 0.0)
            sequences.append({
                'sequence': path,
                'length': len(path),
                'probability': prob,
                'start': path[0],
                'end': path[-1]
            })
        except nx.NetworkXNoPath:
            continue

    return sequences


def build_sequences_dataframes(source_results, sink_results, acts, all_seq=True):
    """
    Constroi dois DataFrames: um para source e outro para sink.

    Parâmetros:
    - source_results: dict com chaves: parent_tree, path_probs, filtered_cond_prob, etc.
    - sink_results: mesmo formato, para sink
    - acts: lista de atos
    - all_seq: se True, tenta extrair sequências para todas as fontes/sumidouros

    Retorna:
    - source_sequences_df, sink_sequences_df
    """
    source_records = []
    sink_records = []

    # EXTRAIR SEQUÊNCIAS SOURCE
    for source in acts:
        # Verifica se temos resultados para esta fonte
        if source in source_results:
            res = source_results[source]
            parent_tree = res['parent']
            path_probs = res['path_probs']
            seqs = extract_sequences_from_ditree(parent_tree, path_probs, acts)
            for s in seqs:
                s['source'] = source
            source_records.extend(seqs)
        else:
            # Pode-se rodar aqui mrditree_source dinamicamente, se necessário
            pass

    # EXTRAIR SEQUÊNCIAS SINK
    for sink in acts:
        if sink in sink_results:
            res = sink_results[sink]
            parent_tree = res['parent']
            path_probs = res['path_probs']
            seqs = extract_sequences_from_ditree(parent_tree, path_probs, acts)
            for s in seqs:
                s['sink'] = sink
            sink_records.extend(seqs)

    # Converter para DataFrames
    df_source = pd.DataFrame(source_records)
    df_sink = pd.DataFrame(sink_records)

    # Expandir a coluna 'sequence' em colunas separadas (opcional, mas útil)
    if not df_source.empty:
        max_len_source = df_source['sequence'].apply(len).max()
        for i in range(max_len_source):
            df_source[f'step_{i + 1}'] = df_source['sequence'].apply(lambda x, idx=i: x[idx] if len(x) > idx else None)

    if not df_sink.empty:
        max_len_sink = df_sink['sequence'].apply(len).max()
        for i in range(max_len_sink):
            df_sink[f'step_{i + 1}'] = df_sink['sequence'].apply(lambda x, idx=i: x[idx] if len(x) > idx else None)

    return df_source, df_sink