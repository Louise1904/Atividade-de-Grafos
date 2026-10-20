from collections import deque
import heapq

# ===== Labirinto =====
labirinto = [
    "I.........",
    ".......##.",
    "..#######.",
    "..#######.",
    "...#####.#",
    "..........",
    ".#######..",
    ".#######..",
    ".#######.#",
    ".........F",
]


def achar(lab, simbolo):
    for i, linha in enumerate(lab):
        if simbolo in linha:
            return (i, linha.index(simbolo))

DIRECOES = [(-1, 0), (0, 1), (1, 0), (0, -1)]   # cima, direita, baixo, esquerda

def livre(lab, i, j):
    dentro = 0 <= i < len(lab) and 0 <= j < len(lab[0])
    return dentro and lab[i][j] != '#'

def montar_grafo(lab):
    grafo = {}
    for i in range(len(lab)):
        for j in range(len(lab[0])):
            if not livre(lab, i, j):
                continue
            grafo[(i, j)] = []
            for di, dj in DIRECOES:
                if livre(lab, i + di, j + dj):
                    grafo[(i, j)].append((i + di, j + dj))
    return grafo

def desenhar(lab, caminho):
    grade = [list(linha) for linha in lab]
    for i, j in caminho:
        if grade[i][j] == '.':
            grade[i][j] = '*'
    for linha in grade:
        print(''.join(linha))

# ===== DFS =====
def dfs(grafo, v, saida, visitados, veio_de):
    visitados.add(v)
    if v == saida:
        return True          # achou a saída
    for w in grafo[v]:
        if w not in visitados:
            veio_de[w] = v   # cheguei em w vindo de v
            if dfs(grafo, w, saida, visitados, veio_de):
                return True  # a chamada de baixo achou, então avisa a de cima
    return False             # testou todos os vizinhos e não achou

# ===== BFS =====
def bfs(grafo, inicio, saida, visitados, veio_de):
    visitados.add(inicio)
    fila = deque([inicio])           # a fila começa com o I
    while fila:
        v = fila.popleft()           # tira o primeiro da fila
        if v == saida:
            return True              # achou a saída
        for w in grafo[v]:
            if w not in visitados:
                visitados.add(w)     # marca ao ENTRAR na fila
                veio_de[w] = v       # cheguei em w vindo de v
                fila.append(w)       # coloca no fim da fila
    return False                     # fila esvaziou e não achou

# ===== Busca gulosa =====
def h(v, saida):                     # distância de Manhattan até a saída
    return abs(v[0] - saida[0]) + abs(v[1] - saida[1])

def gulosa(grafo, inicio, saida, visitados, veio_de):
    visitados.add(inicio)
    fronteira = [(h(inicio, saida), inicio)]      # fila de prioridade: (h, casa)
    while fronteira:
        _, v = heapq.heappop(fronteira)           # tira a casa de MENOR h
        if v == saida:
            return True                           # achou a saída
        for w in grafo[v]:
            if w not in visitados:
                visitados.add(w)                  # marca ao entrar na fronteira
                veio_de[w] = v                    # cheguei em w vindo de v
                heapq.heappush(fronteira, (h(w, saida), w))
    return False                                  # fronteira esvaziou e não achou

# ===== Reconstrução do caminho =====
def reconstruir(veio_de, inicio, saida):
    caminho = [saida]              # começa pelo F
    atual = saida
    while atual != inicio:         # volta até chegar no I
        atual = veio_de[atual]     # "de onde eu vim?"
        caminho.append(atual)
    caminho.reverse()              # estava F → I; agora fica I → F
    return caminho

# ===== Teste DFS =====
print("===== DFS =====")
inicio = achar(labirinto, 'I')
saida = achar(labirinto, 'F')
grafo = montar_grafo(labirinto)

veio_de = {}
visitados = set()
achou = dfs(grafo, inicio, saida, visitados, veio_de)

print("Achou a saída?", achou)
print("Chegou no F vindo de:", veio_de[saida])
print("Casas visitadas:", len(visitados))

caminho = reconstruir(veio_de, inicio, saida)
print("Caminho:", caminho)
print("Casas no caminho:", len(caminho))
desenhar(labirinto, caminho)

# ===== Teste BFS =====
print()
print("===== BFS =====")
veio_de_bfs = {}
visitados_bfs = set()
achou = bfs(grafo, inicio, saida, visitados_bfs, veio_de_bfs)
print("Achou a saída?", achou)
print("Casas visitadas:", len(visitados_bfs))
caminho_bfs = reconstruir(veio_de_bfs, inicio, saida)
print("Casas no caminho:", len(caminho_bfs))
desenhar(labirinto, caminho_bfs)

# ===== Teste gulosa =====
print()
print("===== GULOSA =====")
veio_de_gul = {}
visitados_gul = set()
achou = gulosa(grafo, inicio, saida, visitados_gul, veio_de_gul)
print("Achou a saída?", achou)
print("Casas visitadas:", len(visitados_gul))
caminho_gul = reconstruir(veio_de_gul, inicio, saida)
print("Casas no caminho:", len(caminho_gul))
desenhar(labirinto, caminho_gul)