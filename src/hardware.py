import pandas as pd

####################################################################
# BASES NUMÉRICAS E ELETRICIDADE
#   Converte os endereços dos sensores entre bases e calcula a
# potência do subsistema de comunicação de cada módulo.
####################################################################


## Converte o endereço do sensor para três representações.
## Recebe o código como string hexadecimal (ex: "0x1A2F").
def converter_codigo_sensor(codigo):
    # O segundo argumento do int() é a base em que a string está
    # escrita. Com 16 ele lê hexadecimal e reconhece o prefixo "0x".
    decimal = int(codigo, 16)

    # bin() faz o caminho inverso: do inteiro para string binária.
    return {
        "hexadecimal": codigo,
        "decimal": decimal,
        "binario": bin(decimal),
    }


## Aplica a conversão em todos os módulos da colônia.
def tabela_codigos(df):
    # O par módulo/código se repete em todos os ciclos.
    # drop_duplicates() reduz às combinações únicas.
    codigos = df[["modulo", "codigo_sensor"]].drop_duplicates()
    linhas = []

    for _, linha in codigos.iterrows():
        info = converter_codigo_sensor(linha["codigo_sensor"])
        info["modulo"] = linha["modulo"]   # acrescenta chave ao dicionário já criado
        linhas.append(info)

    # Lista de dicionários vira DataFrame: as chaves viram colunas.
    return pd.DataFrame(linhas)


## Calcula a potência de cada registro de telemetria.
def calcular_potencia(df):
    # Lei de Joule: P = V x I, em watts.
    # Operação vetorizada: o pandas multiplica as colunas linha a linha.
    df["potencia_w"] = df["tensao_v"] * df["corrente_a"]

    return df


## Agrega a potência por módulo.
def resumo_potencia_por_modulo(df):
    resumo = df.groupby("modulo")["potencia_w"].agg(["mean", "max", "std"])

    return resumo