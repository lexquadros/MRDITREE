import pandas as pd
import os
import matplotlib.pyplot as plt
from ditree_resources.ditree_source import ditree_source
from ditree_resources.ditree_sink import ditree_sink
from ditree_resources import plot_tree
from ditree_resources.extract_sequences import build_sequences_dataframes
from ditree_resources.sequence_tools import sequence_to_transition_matrix

def prepare_data(df):
    """
    Prepara os dados para análise de sequência comportamental.
    Lê um DataFrame onde cada coluna representa uma série de comportamentos (sequência).
    A primeira linha de cada coluna é tratada como nome da coluna (ex: nome da espécie).
    Salva cada sequência em um arquivo CSV e organiza em pastas separadas.
    Retorna um DataFrame com todas as sequências.

    Args:
        df (pd.DataFrame): DataFrame com sequências comportamentais. Cada coluna é uma série.
                           A primeira linha contém o nome (label) da coluna (ex: nome da espécie).

    Returns:
        df_spp (pd.DataFrame): DataFrame onde cada coluna é uma sequência comportamental limpa.
    """
    df_spp = pd.DataFrame()

    for col_idx in df.columns:
        col_dados = df[col_idx].to_list()
        nome_coluna = col_dados[0]
        dados_coluna = col_dados[1:]

        # Criar pasta para cada espécie/coluna
        output_dir = f'output/{nome_coluna}'
        os.makedirs(output_dir, exist_ok=True)

        # Gerando sequências e lista de atos comportamentais
        sequence = [x for x in dados_coluna if pd.notna(x) and str(x).strip() != '']

        # Adiciona a sequência como uma nova coluna no df_spp
        # Garante que todas as colunas tenham o mesmo comprimento (preenchendo com None se necessário)
        max_len = max(len(df_spp), len(sequence))
        df_spp = df_spp.reindex(range(max_len))
        df_spp[nome_coluna] = pd.Series(sequence, dtype=object)

        #print(f"Pasta criada: {output_dir}")

        acts_sequence = {f'{nome_coluna}': sequence}
        df_acts_sequence = pd.DataFrame(acts_sequence)
        df_acts_sequence.to_csv(
            f'output/{nome_coluna}/sequence_{nome_coluna}.csv',
            index=False
        )
        #print(acts_sequence)

    return df_spp  # Retorna o DataFrame com todas as sequências


def run_mrditree_analysis_multi_species(df_spp, alpha=0.05, output_base_dir='output'):
    """
    Executa análise MRDITree para múltiplas espécies (colunas do DataFrame).
    Para cada coluna (espécie), executa Source e Sink para todos os atos,
    salva matrizes e gera imagens PNG das árvores em pastas organizadas por espécie.
    Retorna um dicionário com todos os resultados.

    Args:
        df_spp (pd.DataFrame): DataFrame onde cada coluna é uma sequência comportamental.
        alpha (float): Nível de significância para filtrar transições.
        output_base_dir (str): Pasta base para salvar os resultados.

    Returns:
        all_results (dict): {'species_name': {'source_results': ..., 'sink_results': ...}}
    """
    all_results = {}

    for species_name in df_spp.columns: # o loop faz o segue pelas colunas/espécies
        print(f"\n--- Iniciando análise para: {species_name} ---")

        # Extrair sequência e atos para a espécie/coluna
        sequence = df_spp[species_name].dropna().tolist()
        acts = sorted(list(set(sequence)))  # Ordenar para consistência

        if not acts:
            print(f"Nenhum ato encontrado para {species_name}, pulando...")
            continue

        # Criar pasta específica para cada espécie/coluna
        output_dir = os.path.join(output_base_dir, species_name)
        os.makedirs(output_dir, exist_ok=True)

        # --- Executar análise para cada espécie/coluna ---
        species_results = run_single_species_analysis(
            sequence=sequence,
            acts=acts,
            alpha=alpha,
            output_dir=output_dir
        )

        all_results[species_name] = species_results
        print(f"Análise concluída para: {species_name}")

    print("\n=== Análise de todas as espécies concluída ===")
    return all_results


def run_single_species_analysis(sequence, acts, alpha=0.05, output_dir='.'):
    """
    Função auxiliar que executa a análise MRDITree para uma única espécie.
    Mantém a lógica original da função antiga.
    """
    # Matriz de transição observada
    obs_matrix, act_to_idx = sequence_to_transition_matrix(sequence, acts)

    print("Matriz de Transição Observada:")
    print(pd.DataFrame(obs_matrix, index=acts, columns=acts))

    # Salvar matriz de transição
    matrix = pd.DataFrame(obs_matrix, index=acts, columns=acts)
    matrix_path = os.path.join(output_dir, 'matrix_transicao.csv')
    matrix.to_csv(matrix_path)

    # Dicionários para armazenar resultados
    source_results = {}
    sink_results = {}

    # LOOP: Para cada ato como fonte
    for source in acts:
        try:
            parent_tree, path_probs, filtered_cond_prob = ditree_source(obs_matrix, acts, source, alpha=alpha)
            source_results[source] = {
                'parent': parent_tree,
                'path_probs': path_probs,
                'filtered_cond_prob': filtered_cond_prob
            }

            # Salvar imagem da árvore source
            plot_tree.plot_ditree_dendrogram(
                parent_dict=parent_tree,
                transition_probs=filtered_cond_prob,
                acts=acts,
                title=f"MRDITree Source - Dendrograma Hierárquico (Fonte: {source})"
            )
            plt.savefig(os.path.join(output_dir, f'source_{source}.png'), format='png', bbox_inches='tight')
            plt.close()

            print(f"Imagem salva: {output_dir}/source_{source}.png")

            # Salvar a matriz filtrada individualmente para cada fonte
            df_cond = pd.DataFrame(filtered_cond_prob, index=acts, columns=acts)
            df_cond.to_csv(os.path.join(output_dir, f'filtered_cond_prob_source_{source}.csv'))

        except Exception as e:
            print(f"Erro ao processar source {source}: {e}")

    # LOOP: Para cada ato como sumidouro
    for sink in acts:
        try:
            parent_tree, path_probs, filtered_cond_prob = ditree_sink(obs_matrix, acts, sequence, sink, alpha=alpha)
            sink_results[sink] = {
                'parent': parent_tree,
                'path_probs': path_probs,
                'filtered_cond_prob': filtered_cond_prob
            }

            # Salvar imagem da árvore sink
            plot_tree.plot_ditree_dendrogram(
                parent_dict=parent_tree,
                transition_probs=filtered_cond_prob,
                acts=acts,
                title=f"MRDITree Sink - Dendrograma Hierárquico (Sumidouro: {sink})"
            )
            plt.savefig(os.path.join(output_dir, f'sink_{sink}.png'), format='png', bbox_inches='tight')
            plt.close()

            print(f"Imagem salva: {output_dir}/sink_{sink}.png")

            # Salvar a matriz filtrada individualmente para cada sumidouro
            df_cond = pd.DataFrame(filtered_cond_prob, index=acts, columns=acts)
            df_cond.to_csv(os.path.join(output_dir, f'filtered_cond_prob_sink_{sink}.csv'))

        except Exception as e:
            print(f"Erro ao processar sink {sink}: {e}")

    print(f"\nTodas as imagens e matrizes foram salvas em: {output_dir}")

    # gerando dataframes com as sequências mais prováveis
    df_source, df_sink = build_sequences_dataframes(source_results, sink_results, acts)

    df_source_path = os.path.join(output_dir, 'sequences_source.csv')
    df_source.to_csv(df_source_path, index=False)

    df_sink_path = os.path.join(output_dir, 'sequences_sink.csv')
    df_sink.to_csv(df_sink_path, index=False)


    # === Visualizar ===
    # print("\nSequências Source:")
    # print(df_source[['source', 'sequence', 'length', 'probability', 'start', 'end']].head(10))

    # print("\nSequências Sink:")
    # print(df_sink[['sink', 'sequence', 'length', 'probability', 'start', 'end']].head(10))

    return {'source_results': source_results, 'sink_results': sink_results}