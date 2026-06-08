# Imports
import pandas as pd
from utils.data_utils import prepare_data, run_mrditree_analysis_multi_species

# Carregar os dados
file_path = 'sequencias_aves/sequencias_todas.csv'

df = pd.read_csv(file_path, header=None, dtype=str, keep_default_na=False)

# Função para preparar o dataframe
df_analysis = prepare_data(df)

# Executar a análise multi espécies
all_analysis_results = run_mrditree_analysis_multi_species(
    df_spp=df_analysis,
    alpha=0.05,  # Critério de Significância
    output_base_dir='output'
)