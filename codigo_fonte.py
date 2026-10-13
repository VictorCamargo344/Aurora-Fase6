####################################################################
# SCIC — SISTEMA DE COMUNICAÇÃO INTERPLANETÁRIA DA COLÔNIA
#   Ponto de entrada do sistema. Este arquivo não calcula nada:
# ele prepara os dados, monta as estruturas e chama as funções
# dos módulos em src/ conforme a opção escolhida.
####################################################################

from src.dados import carregar_dados, resumir_dados
from src.erros import calcular_erros, resumo_erros_por_modulo
from src.modelo import preparar_dados, treinar_modelo, avaliar_modelo, avaliar_baseline
from src.alertas import construir_heap_alertas, proximo_alerta, listar_alertas
from src.busca import construir_trie
from src.hardware import tabela_codigos, calcular_potencia, resumo_potencia_por_modulo


## Carrega o CSV e acrescenta as colunas derivadas.
## A ordem importa: as colunas de erro precisam existir antes de
## qualquer função que dependa delas.
def preparar_sistema():
    df = carregar_dados()        # 12 colunas do CSV
    df = calcular_erros(df)      # + erro absoluto, relativo e sinalizado
    df = calcular_potencia(df)   # + potencia_w

    return df


## Imprime as opções disponíveis.
def exibir_menu():
    # Aspas triplas permitem string de várias linhas num print só.
    print("""
=== SCIC — Sistema de Comunicação Interplanetária da Colônia ===
1 - Resumo estatístico da telemetria
2 - Erros do sistema atual por módulo
3 - Treinar modelo e comparar com o baseline
4 - Fila de alertas por prioridade
5 - Atender próximo alerta
6 - Buscar módulo ou sensor por prefixo
7 - Tabela de conversão dos códigos de sensor
8 - Consumo energético por módulo
0 - Sair
""")


def main():
    # O estado é montado UMA vez, antes do loop: recarregar o CSV a
    # cada opção seria desperdício, e o heap precisa persistir para
    # que a opção 5 possa consumi-lo aos poucos.
    df = preparar_sistema()
    heap = construir_heap_alertas(df)
    trie_modulos = construir_trie(df, "modulo")
    trie_sensores = construir_trie(df, "codigo_sensor")

    # Loop infinito: só termina quando o usuário escolhe a opção 0.
    while True:
        exibir_menu()
        # strip() remove espaços acidentais antes da comparação.
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            print("\n=== Resumo estatístico da telemetria ===")
            print(resumir_dados(df))

        elif opcao == "2":
            print("\n=== Erros do sistema atual por módulo ===")
            print(resumo_erros_por_modulo(df))

        elif opcao == "3":
            print("\n=== Modelo vs. Baseline ===")
            # O modelo é treinado aqui, e não em preparar_sistema(),
            # para que o custo só ocorra quando o usuário pedir.
            X, y = preparar_dados(df)
            modelo, X_teste, y_teste = treinar_modelo(X, y)
            # As duas avaliações usam as MESMAS linhas de teste,
            # senão a comparação não seria válida.
            print("Modelo:  ", avaliar_modelo(modelo, X_teste, y_teste))
            print("Baseline:", avaliar_baseline(df, X_teste, y_teste))

        elif opcao == "4":
            print("\n=== Fila de alertas por prioridade ===")
            # listar_alertas trabalha numa cópia: o heap não é consumido.
            for alerta in listar_alertas(heap, 5):
                print(alerta)

        elif opcao == "5":
            print("\n=== Próximo alerta ===")
            # Esta opção, sim, remove o alerta da fila.
            alerta = proximo_alerta(heap)
            if alerta is None:
                print("Nenhum alerta pendente.")
            else:
                print(alerta)

        elif opcao == "6":
            print("\n=== Busca por prefixo ===")
            prefixo = input("Prefixo: ").strip()
            # A mesma busca roda nas duas tries: o usuário pode
            # digitar tanto nome de módulo quanto código de sensor.
            print("Módulos: ", trie_modulos.buscar_prefixo(prefixo))
            print("Sensores:", trie_sensores.buscar_prefixo(prefixo))

        elif opcao == "7":
            print("\n=== Tabela de conversão dos códigos de sensor ===")
            print(tabela_codigos(df))

        elif opcao == "8":
            print("\n=== Consumo energético por módulo ===")
            print(resumo_potencia_por_modulo(df))

        elif opcao == "0":
            print("\nEncerrando o SCIC.")
            break

        else:
            print("\nOpção inválida.")


# Garante que o menu só dispare quando o arquivo for executado
# diretamente, e não se algo for importado dele.
if __name__ == "__main__":
    main()