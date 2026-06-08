import networkx as nx
import matplotlib.pyplot as plt

# --------------------- Plot MRDITREE -------------------
def hierarchy_pos(G, root, width=20., vert_gap=2., vert_loc=0, xcenter=0.5):
    """
    Retorna um posicionamento hierárquico para os nós de um grafo direcionado.
    """
    def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None):
        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)

        children = list(G.successors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)

        if len(children) != 0:
            dx = width / len(children)
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                     vert_loc=vert_loc-vert_gap, xcenter=nextx,
                                     pos=pos, parent=root)
        return pos
    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)


def plot_ditree_dendrogram(parent_dict, transition_probs, acts, title="MRDITree - Dendrograma com Probabilidades"):
    """
    Plota o ditree como um dendrograma hierárquico.

    Parâmetros:
    - parent_dict: dict no formato {child: parent}
    - transition_probs: matriz 2D de probabilidades condicionais P(j|i)
    - acts: lista de categorias (nomes dos atos)
    - title: título do gráfico

    Retorna:
    - fig: objeto matplotlib.figure.Figure
    """
    # Mapeamento de nomes para índices
    act_to_idx = {act: i for i, act in enumerate(acts)}

    # Criar grafo direcionado
    G = nx.DiGraph()

    # Adicionar todas as arestas com base no parent_dict
    edges_with_labels = []
    for child, parent in parent_dict.items():
        if parent is not None:
            G.add_edge(parent, child)
            # Obter probabilidade da transição parent → child
            i = act_to_idx[parent]
            j = act_to_idx[child]
            prob = transition_probs[i, j]
            edges_with_labels.append(((parent, child), f"{prob:.3f}"))
        else:
            G.add_node(child)  # sumidouro ou raiz

    # Encontrar a raiz (nó sem pai) para layouts hierárquicos
    root_candidates = [node for node in G.nodes if G.in_degree(node) == 0]
    root = root_candidates[0] if root_candidates else None

    # Se não houver nó sem entrada (ex: sink solution), definir o sumidouro como "raiz visual"
    if not root:
        # Em sink solution, o sumidouro é o destino final → usei como raiz do dendrograma invertido
        sink = [node for node in parent_dict if parent_dict[node] is None]
        if sink:
            root = sink[0]
        else:
            root = acts[0]  # fallback

    # Layout hierárquico (de cima para baixo)
    try:
        pos = hierarchy_pos(G, root, width=20., vert_gap=2.5)
    except:
        pos = nx.spring_layout(G, seed=42)
        print("Layout hierárquico falhou. Usando spring layout.")

    # Criar figura
    fig, ax = plt.subplots(figsize=(12, 8))

    # Nós
    nx.draw_networkx_nodes(G, pos, node_size=1500, node_color='lightsteelblue', edgecolors='black', linewidths=1.5, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold', ax=ax)

    # Arestas
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=20, width=1.5, ax=ax)

    # Rótulos das arestas (probabilidades)
    edge_labels = dict(edges_with_labels)
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=12, font_color='darkred', ax=ax)

    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.axis('off')
    fig.tight_layout()

    return fig
