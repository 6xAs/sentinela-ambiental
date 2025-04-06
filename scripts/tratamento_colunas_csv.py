import pandas as pd

# Carregar o arquivo CSV
df = pd.read_csv(
    './data/brutos/dados_meteorologicos_regiao_norte/precipitacoes_2023_2024/precipitacoes_2023_RO/INMET_N_RO_A925_PORTO VELHO_01-01-2023_A_31-12-2023.CSV', 
    sep=';', 
    encoding='latin1',
    na_values=['', ' ', 'NaN', 'NA']  # Identificar diferentes representações de valores vazios
)

# Remover colunas completamente nulas
df = df.dropna(axis=1, how='all')

# Verificar o número de colunas carregadas após a remoção
print(f"Número de colunas válidas: {len(df.columns)}")
print(f"Colunas válidas: {df.columns.tolist()}")

# Substituir o cabeçalho original pelos novos nomes
novos_nomes_colunas = [
    'data',
    'hora_utc',
    'precipitacao_total_horario_mm',
    'pressao_atm_nivel_estacao_horaria_mb',
    'pressao_atm_max_hora_anterior_mb',
    'pressao_atm_min_hora_anterior_mb',
    'radiacao_global_kj_m2',
    'temp_ar_bulbo_seco_horaria_c',
    'temp_ponto_orvalho_c',
    'temp_max_hora_anterior_c',
    'temp_min_hora_anterior_c',
    'temp_orvalho_max_hora_anterior_c',
    'temp_orvalho_min_hora_anterior_c',
    'umidade_rel_max_hora_anterior_pct',
    'umidade_rel_min_hora_anterior_pct',
    'umidade_rel_ar_horaria_pct',
    'vento_direcao_horaria_graus',
    'vento_rajada_maxima_ms',
    'vento_velocidade_horaria_ms',
    'coluna_extra_1',
    'coluna_extra_2'
]

# Ajustar o número de nomes de colunas para corresponder às colunas válidas
novos_nomes_colunas = novos_nomes_colunas[:len(df.columns)]

# Renomear as colunas
df.columns = novos_nomes_colunas

# Substituir valores nulos por 'N'
df.fillna('N', inplace=True)

# Adicionar novas colunas
# 1. Coluna com valor padrão
df['origem_dados'] = 'INMET'

# 2. Coluna calculada: diferença entre temperatura máxima e mínima
if 'temp_max_hora_anterior_c' in df.columns and 'temp_min_hora_anterior_c' in df.columns:
    df['amplitude_termica'] = pd.to_numeric(df['temp_max_hora_anterior_c'], errors='coerce') - pd.to_numeric(df['temp_min_hora_anterior_c'], errors='coerce')

# 3. Coluna calculada: média de umidade relativa
if 'umidade_rel_max_hora_anterior_pct' in df.columns and 'umidade_rel_min_hora_anterior_pct' in df.columns:
    df['umidade_rel_media_pct'] = (
        pd.to_numeric(df['umidade_rel_max_hora_anterior_pct'], errors='coerce') +
        pd.to_numeric(df['umidade_rel_min_hora_anterior_pct'], errors='coerce')
    ) / 2

# Exportar para CSV
df.to_csv(
    './data/processados/dados_meteo_colunas_tratadas_porto_velho_2023_com_colunas_validas.csv', 
    sep=';', 
    index=False, 
    header=True, 
    encoding='utf-8'
)

print(f'Dados salvos com sucesso em: ./data/processados/dados_meteo_colunas_tratadas_porto_velho_2023_com_colunas_validas.csv')