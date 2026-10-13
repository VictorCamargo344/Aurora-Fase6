from src.dados import carregar_dados, resumir_dados
from src.erros import calcular_erros, resumo_erros_por_modulo
from src.modelo import preparar_dados, treinar_modelo, avaliar_modelo, avaliar_baseline
from src.alertas import construir_heap_alertas, proximo_alerta, listar_alertas
from src.busca import construir_trie
from src.hardware import tabela_codigos, calcular_potencia, resumo_potencia_por_modulo


def preparar_sistema():
    df = carregar_dados()
    df = calcular_erros(df)
    df = calcular_potencia(df)

    return df


def exibir_menu():
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
    df = preparar_sistema()
    heap = construir_heap_alertas(df)
    trie_modulos = construir_trie(df, "modulo")
    trie_sensores = construir_trie(df, "codigo_sensor")

    while True:
        exibir_menu()
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            print("\n=== Resumo estatístico da telemetria ===")
            print(resumir_dados(df))
        elif opcao == "2":
            print("\n=== Resumo de erros por módulo ===")
            print(resumo_erros_por_modulo(df))
        elif opcao == "0":
            print("\nEncerrando o SCIC.")
            break
        else:
            print("\nOpção inválida.")


if __name__ == "__main__":
    main()