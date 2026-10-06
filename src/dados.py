import os
import pandas as pd


PASTA_SRC = os.path.dirname(os.path.abspath(__file__))
## dirname utilizado para chegar na pasta raiz do projeto
PASTA_RAIZ = os.path.dirname(PASTA_SRC)
# join utilizado para remontar o caminho do arquivo csv com os dados
ARQUIVO_CSV = os.path.join(PASTA_RAIZ, "data", "dados_aurora_siger.csv")

## Função para carregar os dados
def carregar_dados():
    df = pd.read_csv(ARQUIVO_CSV)
    return df
