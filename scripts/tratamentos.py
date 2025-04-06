import pandas as pd
from io import StringIO

# Caminho para o arquivo original
arquivo_original = "./data/brutos/dados_meteorologicos_regiao_norte/precipitacoes_2023_2024/precipitacoes_2023_RO/INMET_N_RO_A925_PORTO VELHO_01-01-2023_A_31-12-2023.CSV"

# Abrir o arquivo original
with open(arquivo_original, "r", encoding="latin1") as f:
    linhas = f.readlines()

# Extrair o cabeçalho de dados (linha 9 do arquivo original)
cabecalho_bruto = linhas[8].strip().split(";")
cabecalho_limpo = [
    col.encode('latin1').decode('utf-8', errors='ignore').strip().lower().replace(" ", "_")
    for col in cabecalho_bruto
]

# Linhas válidas com o número correto de colunas
linhas_validas = [
    linha for linha in linhas[9:]
    if len(linha.strip().split(";")) == len(cabecalho_limpo)
]

# Criar CSV em memória
csv_limpo = StringIO()
csv_limpo.write(";".join(cabecalho_limpo) + "\n")
csv_limpo.writelines(linhas_validas)
csv_limpo.seek(0)

# Carregar no pandas
df = pd.read_csv(csv_limpo, sep=";", decimal=",", encoding="utf-8")

# Exportar para novo arquivo
nome_saida = "./data/processados/inmet_porto_velho_2023_limpo.csv"
df.to_csv(nome_saida, index=False, encoding="utf-8")

print(f"Arquivo limpo salvo como: {nome_saida}")
