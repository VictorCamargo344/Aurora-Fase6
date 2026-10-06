import pandas as pd


def calcular_erros(df):
    df["erro_absoluto"] = (df["latencia_observada_ms"] - df["latencia_prevista_ms"]).abs()
    df["erro_relativo"] = (df["erro_absoluto"] / df["latencia_observada_ms"]) * 100
    df["erro_sinalizado"] = df["latencia_observada_ms"] - df["latencia_prevista_ms"]
    return df


def resumo_erros_por_modulo(df):
    erro_por_modulo = df.groupby("modulo")["erro_relativo"].agg(["mean", "max", "median", "min"])
    return erro_por_modulo