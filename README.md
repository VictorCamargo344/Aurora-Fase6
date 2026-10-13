# SCIC — Sistema de Comunicação Interplanetária da Colônia

Fase 6 do projeto Aurora Siger (FIAP). Sistema em Python que organiza a telemetria de comunicação de uma colônia marciana, avalia a confiabilidade das previsões do sistema atual, treina um modelo alternativo, prioriza alertas críticos e permite busca por prefixo.

O projeto dá continuidade às fases anteriores: os seis módulos (Habitat Alpha, MedBase, Reator Solar, BioLab, LogiStore e TerraBot) são os mesmos cadastrados na Fase 2, monitorados energeticamente na Fase 3, conectados em rede na Fase 4 e analisados pelo núcleo cognitivo na Fase 5.

## Como executar

```bash
pip install pandas numpy matplotlib seaborn scikit-learn
python codigo_fonte.py
```

O sistema abre um menu no terminal. Todas as opções operam sobre a base já carregada em memória.

## Dependências

| Biblioteca | Uso no projeto |
|---|---|
| pandas | leitura do CSV, agregações e filtros |
| numpy | raiz quadrada no cálculo do RMSE |
| scikit-learn | divisão treino/teste, regressão linear e métricas |

Todas foram trabalhadas na fase. Não há bibliotecas externas ao conteúdo estudado — `heapq` e `os` fazem parte da biblioteca padrão do Python.

## Estrutura dos arquivos
Aurora-Fase6/
├── codigo_fonte.py # menu e integração dos módulos
├── data/
│ └── dados_aurora_siger.csv # base simulada (504 registros)
├── src/
│ ├── init.py
│ ├── dados.py # carga e resumo estatístico
│ ├── erros.py # erro absoluto, relativo e sinalizado
│ ├── modelo.py # treino, métricas e baseline
│ ├── alertas.py # fila de prioridade (heap)
│ ├── busca.py # busca por prefixo (trie)
│ └── hardware.py # bases numéricas e potência
└── README.md


A separação entre `codigo_fonte.py` e `src/` é deliberada: o arquivo principal não calcula nada, apenas chama as funções dos módulos e organiza a interação com o usuário. Cada módulo de `src/` resolve um problema e pode ser testado isoladamente.

## A base de dados

504 registros de telemetria: 84 ciclos para cada um dos seis módulos. As doze colunas incluem identificação do módulo, código do sensor em hexadecimal, distância em metros, qualidade do sinal, status operacional, carga de tráfego, tensão, corrente, latência observada e latência prevista pelo sistema atual da colônia.

A base é simulada. A latência observada foi gerada como função da distância, da qualidade do sinal, do status e da carga de tráfego, somada a ruído aleatório. A latência prevista representa o sistema antigo da colônia, que estima a latência apenas pela distância.

## Menu

| Opção | Função |
|---|---|
| 1 | Resumo estatístico da telemetria |
| 2 | Erros do sistema atual por módulo |
| 3 | Treinar modelo e comparar com o baseline |
| 4 | Fila de alertas por prioridade |
| 5 | Atender próximo alerta |
| 6 | Buscar módulo ou sensor por prefixo |
| 7 | Tabela de conversão dos códigos de sensor |
| 8 | Consumo energético por módulo |
| 9 | Análise final dos resultados |
| 0 | Sair |

## Decisões técnicas

**Três medidas de erro, com papéis distintos.** O erro sinalizado preserva o sinal e decide *quais* ciclos viram alerta — erro negativo significa que o sistema foi pessimista e a comunicação foi melhor que o previsto, o que não é problema operacional. O erro absoluto define a *prioridade* na fila. O erro relativo permite comparar módulos com escalas de latência diferentes.

**Limiar de alerta em 60 ms.** Corresponde ao percentil 90 do erro sinalizado, concentrando a fila nos ciclos mais críticos. Um limiar mais baixo marcava 78% dos registros como alerta, o que inviabiliza uma fila de prioridade.

**Heap em vez de lista ordenada.** A fila recebe registros continuamente e precisa entregar sempre o caso mais grave. O heap insere e remove em tempo logarítmico sem manter o restante ordenado. Como o `heapq` do Python implementa heap de mínimo, o erro é armazenado negativado para que o maior saia primeiro.

**Trie para busca por prefixo.** Os códigos de sensor seguem um padrão de zona: o primeiro dígito hexadecimal indica a faixa de distância do módulo. Buscar `0x1` devolve o anel interno, `0x3` os periféricos. Numa lista, a busca percorreria todos os registros; na trie, o custo depende do tamanho do prefixo.

## Limitações conhecidas

- A busca por prefixo é sensível a maiúsculas: `Terra` encontra o TerraBot, `terra` não.
- O modelo é uma regressão linear simples, sem validação cruzada nem busca de hiperparâmetros.
- A base é simulada e não representa condições reais de comunicação interplanetária.
- O heap é reconstruído a cada execução; alertas atendidos não são persistidos.

## Equipe

Ellen Kauane Rodrigues Alves, Rafael Gonçalves de Souza Pereira, Pietra Fanticelli e Victor de Camargo Gomes.
