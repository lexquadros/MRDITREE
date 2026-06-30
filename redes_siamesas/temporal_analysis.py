# notebook code3
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from scipy.spatial.distance import jensenshannon
import warnings
warnings.filterwarnings('ignore')



# ============================================
# 1. ANALISADOR TEMPORAL (CADEIAS DE MARKOV)
# ============================================

class TemporalAnalyzer:
    """Analisa padrões de transição e dinâmica temporal das sequências"""

    def __init__(self, sequences, labels, vocab):
        """
        Args:
            sequences: Lista de listas de índices inteiros (sequências codificadas)
            labels: Lista de strings com os nomes das espécies correspondentes
            vocab: Dicionário {comportamento: índice} do SequenceProcessor
        """
        self.sequences = sequences
        self.labels = labels
        self.vocab = vocab
        self.reverse_vocab = {v: k for k, v in vocab.items()}
        self.vocab_size = len(vocab)

        # Dicionário para armazenar matrizes de transição por espécie
        self.transition_matrices = {}
        self._build_all_matrices()

    def _build_all_matrices(self):
        """Constrói a matriz de transição de probabilidade para cada espécie"""
        species_sequences = {}

        # Agrupa sequências por espécie
        for seq, label in zip(self.sequences, self.labels):
            if label not in species_sequences:
                species_sequences[label] = []
            species_sequences[label].append(seq)

        # Calcula matriz para cada espécie
        for species, seqs in species_sequences.items():
            self.transition_matrices[species] = self._compute_markov_matrix(seqs)

    def _compute_markov_matrix(self, sequences, smoothing=1e-4):
        """
        Calcula a matriz de transição de Markov (P(t|t-1))
        Aplica suavização de Laplace para evitar probabilidades zero.
        """
        # Matriz de contagem N x N
        counts = np.zeros((self.vocab_size, self.vocab_size))

        for seq in sequences:
            for i in range(len(seq) - 1):
                current_state = seq[i]
                next_state = seq[i+1]

                # Ignora tokens de padding (índice 0)
                if current_state == 0 or next_state == 0:
                    continue

                counts[current_state, next_state] += 1

        # Suavização de Laplace (evita divisões por zero e probs nulas)
        counts += smoothing

        # Normaliza pelas linhas para obter probabilidades
        row_sums = counts.sum(axis=1, keepdims=True)
        transition_probs = counts / row_sums

        return transition_probs

    def compare_species_transitions(self, species1, species2):
        """
        Compara a similaridade das regras de transição entre duas espécies
        usando a Divergência de Jensen-Shannon (simétrica e limitada entre 0 e 1).
        """
        mat1 = self.transition_matrices[species1]
        mat2 = self.transition_matrices[species2]

        # Calcula JS divergence para cada linha (estado) e tira a média
        js_distances = []
        for i in range(self.vocab_size):
            # Ignora estados que são apenas padding ou não ocorrem
            if self.reverse_vocab[i] == '<PAD>':
                continue

            js_dist = jensenshannon(mat1[i], mat2[i], base=2)
            js_distances.append(js_dist)

        mean_js_distance = np.mean(js_distances)
        similarity_score = 1.0 - mean_js_distance  # Converte distância em similaridade

        return similarity_score, mean_js_distance

    def extract_top_motifs(self, n=3, top_k=10, species=None):
        """
        Extrai os N-grams (motivos) mais frequentes nas sequências.
        n: tamanho do motivo (2 = bigrama, 3 = trigrama)
        """
        motif_counter = Counter()

        target_seqs = self.sequences
        if species:
            target_seqs = [seq for seq, label in zip(self.sequences, self.labels) if label == species]

        for seq in target_seqs:
            # Remove paddings para análise limpa
            clean_seq = [state for state in seq if state != 0]

            for i in range(len(clean_seq) - n + 1):
                motif = tuple(clean_seq[i:i+n])
                motif_counter[motif] += 1

        # Converte índices de volta para nomes de comportamentos
        top_motifs = []
        for motif, count in motif_counter.most_common(top_k):
            behavior_names = [self.reverse_vocab[state] for state in motif]
            top_motifs.append({
                'motif': ' -> '.join(behavior_names),
                'count': count,
                'frequency': count / sum(motif_counter.values())
            })

        return pd.DataFrame(top_motifs)

    def plot_transition_network(self, species, top_k_transitions=15, figsize=(10, 8)):
        """
        Plota um grafo direcionado das transições mais frequentes de uma espécie.
        """
        matrix = self.transition_matrices[species]

        # Extrai todas as transições e ordena por probabilidade
        transitions = []
        for i in range(self.vocab_size):
            for j in range(self.vocab_size):
                if i == 0 or j == 0:  # Ignora padding
                    continue
                prob = matrix[i, j]
                if prob > 0.01:  # Filtro mínimo para evitar ruído visual
                    transitions.append({
                        'source': self.reverse_vocab[i],
                        'target': self.reverse_vocab[j],
                        'weight': prob
                    })

        # Ordena e pega os top K
        transitions = sorted(transitions, key=lambda x: x['weight'], reverse=True)[:top_k_transitions]

        # Cria o grafo NetworkX
        G = nx.DiGraph()
        for t in transitions:
            G.add_edge(t['source'], t['target'], weight=t['weight'])

        # Layout do grafo
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)

        # Tamanhos e cores baseados no grau dos nós
        degrees = [G.degree(n) for n in G.nodes()]
        node_sizes = [d * 500 + 500 for d in degrees]

        # Desenha nós
        nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='lightblue',
                               edgecolors='darkblue', linewidths=1.5)

        # Desenha arestas (espessura proporcional ao peso)
        weights = [G[u][v]['weight'] * 5 for u, v in G.edges()]
        nx.draw_networkx_edges(G, pos, width=weights, edge_color='gray',
                               arrows=True, arrowsize=20, alpha=0.7)

        # Desenha rótulos
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

        # Desenha pesos nas arestas
        edge_labels = {(u, v): f"{G[u][v]['weight']:.2f}" for u, v in G.edges()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

        plt.title(f'Rede de Transição Comportamental: {species}', fontsize=14, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(f'transition_network_{species.replace(" ", "_")}.png', dpi=300, bbox_inches='tight')
        plt.show()

        return G

    def plot_matrix_heatmap(self, species, figsize=(10, 8)):
        """Plota a matriz de transição completa como heatmap"""
        matrix = self.transition_matrices[species]

        # Filtra apenas comportamentos que aparecem como origem (soma da linha > 0)
        active_states = [i for i in range(self.vocab_size) if matrix[i].sum() > 0.01 and i != 0]
        active_names = [self.reverse_vocab[i] for i in active_states]

        filtered_matrix = matrix[np.ix_(active_states, active_states)]

        plt.figure(figsize=figsize)
        sns.heatmap(
            filtered_matrix,
            xticklabels=active_names,
            yticklabels=active_names,
            cmap='Blues',
            annot=True,
            fmt='.2f',
            cbar_kws={'label': 'Probabilidade de Transição'}
        )
        plt.title(f'Matriz de Transição de Markov: {species}', fontsize=14)
        plt.xlabel('Próximo Comportamento', fontsize=12)
        plt.ylabel('Comportamento Atual', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.savefig(f'markov_matrix_{species.replace(" ", "_")}.png', dpi=300, bbox_inches='tight')
        plt.show()


# ============================================
# 2. EXEMPLO DE INTEGRAÇÃO NO SCRIPT PRINCIPAL
# ============================================

def run_temporal_analysis(processor, sequences, species_labels):
    """Função auxiliar para rodar a análise temporal"""
    print("\n" + "="*50)
    print("INICIANDO ANÁLISE TEMPORAL (CADEIAS DE MARKOV)")
    print("="*50)

    analyzer = TemporalAnalyzer(sequences, species_labels, processor.vocab)

    # 1. Extrair motivos (N-grams) globais
    print("\n--- Top 10 Motivos Comportamentais (Trigramas) Globais ---")
    motifs_df = analyzer.extract_top_motifs(n=3, top_k=10)
    print(motifs_df.to_string(index=False))

    # 2. Comparar espécies aleatórias (exemplo)
    unique_species = list(set(species_labels))
    if len(unique_species) >= 2:
        sp1, sp2 = unique_species[0], unique_species[1]
        sim, dist = analyzer.compare_species_transitions(sp1, sp2)
        print(f"\n--- Comparação de Regras de Transição ---")
        print(f"Espécies: {sp1} vs {sp2}")
        print(f"Similaridade das transições (0 a 1): {sim:.4f}")
        print(f"Divergência JS: {dist:.4f}")

    # 3. Gerar visualizações para as 2 primeiras espécies (como exemplo)
    for species in unique_species[:2]:
        print(f"\nGerando visualizações para: {species}")
        analyzer.plot_matrix_heatmap(species)
        analyzer.plot_transition_network(species, top_k_transitions=12)

        # Motivos específicos desta espécie
        print(f"Top 5 motivos para {species}:")
        sp_motifs = analyzer.extract_top_motifs(n=2, top_k=5, species=species)
        print(sp_motifs[['motif', 'frequency']].to_string(index=False))

# ============================================
# COMO USAR NO SEU SCRIPT PRINCIPAL
# ============================================
# No final do seu script `main()` original, adicione:
#
# print("Iniciando análise temporal...")
# run_temporal_analysis(processor, sequences, species_labels)