import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def preparar_dados (df):
    X = pd.get_dummies(df[["distancia_m", "qualidade_sinal_pct", "status", "carga_trafego"]], columns=["status"])
    y = df["latencia_observada_ms"]

    return X, y


def treinar_modelo(X, y):
    X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.2, random_state=42)
    modelo = LinearRegression()
    modelo.fit(X_treino, y_treino)

    return modelo, X_teste, y_teste


def calcular_metricas(y_real, y_prev):
    mae = mean_absolute_error(y_real, y_prev)
    mse = mean_squared_error(y_real, y_prev)
    rmse = float(np.sqrt(mse))
    r2 = r2_score(y_real, y_prev)
    return {
        "MAE": mae,
        "MSE": mse,
        "RMSE": rmse,
        "R2": r2,
    }


def avaliar_modelo(modelo, X_teste, y_teste):
    y_pred = modelo.predict(X_teste)
    
    return calcular_metricas(y_teste, y_pred)


def avaliar_baseline(df, X_teste, y_teste):
    y_baseline = df.loc[X_teste.index, "latencia_prevista_ms"]

    return calcular_metricas(y_teste, y_baseline)
