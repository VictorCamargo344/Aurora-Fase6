import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


def preparar_dados (df):
    X = pd.get_dummies(df[["distancia_m", "qualidade_sinal_pct", "status", "carga_trafego"]], columns=["status"])
    y = df["latencia_observada_ms"]

    return X, y


def treinar_modelo(X, y):
    X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.2, random_state=42)
    modelo = LinearRegression()
    modelo.fit(X_treino, y_treino)

    return modelo, X_teste, y_teste

