import heapq

# Limiar de atraso (ms) a partir do qual um registro vira alerta.
# Constante no topo para ser fácil de ajustar sem caçar número solto no código.
LIMITE_ALERTA_MS = 60.0


## Monta a fila de prioridade a partir dos registros com atraso relevante.
## Recebe o df já processado pelo erros.py (precisa das colunas de erro).
def construir_heap_alertas(df, limite=LIMITE_ALERTA_MS):
    alertas = []   # em Python um heap é uma lista comum; quem dá a estrutura é o heapq

    # Só erro sinalizado POSITIVO vira alerta: significa que a latência real
    # ficou acima da prevista. Erro negativo é previsão pessimista — a
    # comunicação foi melhor que o esperado, não há o que tratar.
    criticos = df[df["erro_sinalizado"] > limite]

    for _, linha in criticos.iterrows():
        # O heapq do Python só faz heap de MÍNIMO. Guardando o erro absoluto
        # negativado, o maior erro vira o menor número e sai primeiro.
        # A ordem da tupla importa: o heap compara da esquerda para a direita,
        # então a prioridade tem que ser o primeiro elemento.
        item = (-linha["erro_absoluto"], linha["modulo"], int(linha["ciclo"]), linha["erro_sinalizado"])
        heapq.heappush(alertas, item)   # inserção em O(log n), sem reordenar a lista

    return alertas


## Retira e devolve o alerta mais grave da fila.
def proximo_alerta(heap):
    if not heap:          # fila vazia: nada a tratar
        return None

    erro_neg, modulo, ciclo, sinalizado = heapq.heappop(heap)

    # Desfaz a inversão de sinal aqui dentro, para quem chama a função
    # receber o erro positivo e nem precisar saber do truque do heap.
    return {
        "Modulo": modulo,
        "Ciclo": ciclo,
        "Erro absoluto": -erro_neg,
        "Erro sinalizado": sinalizado,
    }


## Lista os N alertas mais graves SEM consumir a fila original.
def listar_alertas(heap, n=5):
    # heappop remove de verdade. Trabalhando numa cópia, o heap original
    # continua intacto e o menu pode chamar esta função quantas vezes quiser.
    copia = list(heap)
    resultado = []

    # Para quando acabarem os alertas ou quando já tiver os N pedidos.
    while len(copia) > 0 and len(resultado) < n:
        resultado.append(proximo_alerta(copia))

    return resultado