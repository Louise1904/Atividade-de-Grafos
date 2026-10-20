# Saindo do labirinto: DFS, BFS e Busca Gulosa

Atividade da **Aula 9** de Algoritmos e Estruturas de Dados II (AEDII).

O objetivo é encontrar a saída de um labirinto tratando-o como um **grafo**: cada casa livre é um vértice, e duas casas livres vizinhas são ligadas por uma aresta. Encontrar a saída é buscar um caminho no grafo. O mesmo labirinto é resolvido com três algoritmos (DFS, BFS e Busca Gulosa), e os resultados são comparados.

## Como executar

Requisito: Python 3 (só bibliotecas padrão: `collections` e `heapq`).

```bash
python labirinto.py
```

O programa desenha o caminho encontrado por cada algoritmo e, no final, imprime a tabela comparativa.

## O labirinto

Labirinto próprio de **10 × 10**, na notação da aula:

| Símbolo | Significado |
|---|---|
| `I` | início (entrada), em (0, 0) |
| `F` | fim (saída), em (9, 9) |
| `#` | parede |
| `.` | casa livre |

```
I.........
.......##.
..#######.
..#######.
...#####.#
..........
.#######..
.#######..
.#######.#
.........F
```

Decisões de projeto:

- **Duas rotas de tamanhos diferentes**: uma longa, saindo do I pela direita (o lado que a DFS testa primeiro), e uma curta, pela esquerda e pelo meio.
- **Becos sem saída**: a parede em (4, 9) transforma o alto da coluna da direita em um beco. A casa (4, 8) também é um beco pequeno.
- **Armadilha para a gulosa**: a parede em (8, 9) fica logo acima do F, bloqueando quem chega pela coluna da direita.

## Implementação

As funções `montar_grafo` e `desenhar` foram reaproveitadas da aula sem alteração. O grafo é um dicionário de listas de adjacência, em que os vértices são tuplas `(linha, coluna)`. A ordem dos vizinhos segue `DIRECOES`: cima, direita, baixo, esquerda.

Os três algoritmos têm a mesma assinatura e devolvem `(caminho, casas_visitadas)`:

```python
caminho, casas_visitadas = dfs(grafo, inicio, saida)
caminho, casas_visitadas = bfs(grafo, inicio, saida)
caminho, casas_visitadas = gulosa(grafo, inicio, saida)
```

| Algoritmo | Estrutura | Próximo a sair | Conhece o destino? | Garante o menor caminho? |
|---|---|---|---|---|
| **DFS** | pilha (a própria recursão) | o último descoberto | não | não |
| **BFS** | fila (`deque`) | o primeiro descoberto | não | sim (grafo sem pesos) |
| **Gulosa** | fila de prioridade (`heapq`) | o de menor `h` | sim | não |

- **DFS**: avança o mais fundo possível pelo primeiro vizinho ainda não visitado. Ao chegar num beco, devolve `False` e volta até a última casa com opção não testada.
- **BFS**: visita as casas em camadas de distância a partir do início. A casa é marcada como visitada ao **entrar** na fila, para nenhuma entrar duas vezes.
- **Busca Gulosa**: sempre expande a casa com o menor `h`, a distância de Manhattan até a saída (`|Δlinha| + |Δcoluna|`), que ignora as paredes.

### Reconstrução do caminho

Durante a busca, cada casa descoberta guarda de onde veio, no dicionário `veio_de`:

```python
veio_de[w] = v   # cheguei em w vindo de v
```

Ao chegar no F, a função `reconstruir` segue essas anotações de trás para frente, do F até o I, e inverte a lista com `reverse()`. A mesma função serve para os três algoritmos.

**Casas visitadas** = casas que o algoritmo de fato processou (tirou da pilha, da fila ou da fronteira).

## Resultados

### Caminhos encontrados (`*` = caminho)

**DFS**

```
I******...
.******##.
.*#######.
.*#######.
.**#####.#
..********
.#######.*
.#######**
.#######*#
........*F
```

**BFS**

```
I*........
.*.....##.
.*#######.
.*#######.
.**#####.#
..*******.
.#######*.
.#######*.
.#######*#
........*F
```

**Busca Gulosa**

```
I*........
.*.....##.
.*#######.
.*#######.
.**#####.#
..********
.#######.*
.#######**
.#######*#
........*F
```

### Tabela comparativa

| Algoritmo | Casas no caminho | Passos | Casas visitadas |
|---|---:|---:|---:|
| DFS | 31 | 30 | 39 |
| BFS | **19** | **18** | 56 |
| Busca Gulosa | 21 | 20 | **37** |


