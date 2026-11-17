from collections import deque
import math

class Grafo():

    #construtor da classe grafo
    def __init__(self, vertices, arestas, matriz):
        self.vertices = vertices
        self.arestas = arestas
        self.matriz = matriz


    #retorna o numero de vertices
    def ordem(self):
        return self.vertices

    #retorna o numero de arestas
    def tamanho(self):
        return self.arestas

    #retorna a densidade, ou seja: (2.n_arestas) / (vertices.(vertices-1))
    def densidade(self):
        num_arestas = self.tamanho()
        num_vertices = self.ordem()

        densidade = (2 * num_arestas) / ((num_vertices)*(num_vertices - 1))

        return densidade

    #pega os vizinhos. a logica é: se o vertice atual, junto com o vertice do for, tiver peso diferente de 0, sao vizinhos.
    def vizinhos(self, vertice):
        index = vertice - 1

        vizinhos = []

        for i in range(self.vertices):
            if (self.matriz[index][i] != 0 and
               self.matriz[i][index] != 0 and
               self.matriz[i][index] == self.matriz[index][i]):
                
                vizinhos.append(i + 1)

        return vizinhos

    #para saber o grau é so contar os vizinhos
    def grau_vertice(self, vertice):
        return len(self.vizinhos(vertice=vertice))

    #funcao utilitaria de busca em profundidade
    def __busca_em_profundidade(self, atual, visitado, removido=-1):
            visitado[atual] = True
    
            for vizinho in range(self.vertices):
                if (vizinho != removido
                        and self.matriz[atual][vizinho] != 0
                        and not visitado[vizinho]):
    
                    self.__busca_em_profundidade(vizinho, visitado, removido)
    
    #funcao utilitaria que usa a busca em profudidade para contar os componentes
    def __contar_componentes(self, removido=-1):
        n = self.vertices
        visitado = [False] * n
        componentes = 0

        for v in range(n):
            if v != removido and not visitado[v]:
                componentes += 1
                self.__busca_em_profundidade(v, visitado, removido)

        return componentes

    #returna true para um vertice que é articulacao e false para um que não é
    def vertice_eh_articulacao(self, vertice):
        v1 = self.__contar_componentes(vertice-1)
        v2 = self.__contar_componentes()

        return True if v1 > v2 else False

    #algoritmo de busca em largura, usando fila. retorna a sequencia de vertices visitados e as arestas de retorno
    def busca_largura(self, vertice):
        vertice = vertice - 1

        visitados = [False] * self.vertices

        sequencia_visitados = []
        arestas_arvore = set()
        todas_arestas = set()

        # Mapeia todas as arestas únicas do grafo
        for i in range(self.vertices):
            for j in range(i, self.vertices):
                if self.matriz[i][j] != 0:
                    todas_arestas.add((i, j))

        # O vértice informado é o primeiro ponto de partida.
        # Os demais cobrem os outros componentes.
        pontos_de_partida = [vertice] + [v for v in range(self.vertices) if v != vertice]

        for inicio in pontos_de_partida:
            if visitados[inicio]:
                continue

            visitados[inicio] = True
            fila = deque([inicio])

            while fila:
                vertice_atual = fila.popleft()
                sequencia_visitados.append(vertice_atual)

                for vizinho in range(self.vertices):
                    if self.matriz[vertice_atual][vizinho] != 0:
                        if not visitados[vizinho]:
                            visitados[vizinho] = True
                            fila.append(vizinho)

                            aresta_arvore = (
                                min(vertice_atual, vizinho),
                                max(vertice_atual, vizinho)
                            )

                            arestas_arvore.add(aresta_arvore)

        # Descobrimos as arestas que não fazem parte da árvore
        arestas_retorno = todas_arestas - arestas_arvore

        # Convertendo para vértices com base 1
        sequencia_visitados = [v + 1 for v in sequencia_visitados]

        arestas_retorno = sorted(
            (a + 1, b + 1)
            for a, b in arestas_retorno
        )

        return sequencia_visitados, arestas_retorno

    #funcao de verificar quanto componentes conexo ha no grafo
    def componentes_conexas(self):
        n = self.ordem()

        #copia a matriz de adjacencia
        matriz = [linha[:] for linha in self.matriz]

        #roy-warshall: gera a matriz de alcancabilidade
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if matriz[i][k] != 0 and matriz[k][j] != 0:
                        matriz[i][j] = 1

        #o vertice é alcancavel por ele mesmo
        for i in range(n):
            matriz[i][i] = 1

        #descobre os componentes
        visitados = [False] * n
        componentes = []

        for i in range(n):
            if not visitados[i]:
                componente = []
                for j in range(n):
                    if matriz[i][j] != 0:
                        componente.append(j + 1)
                        visitados[j] = True

                componentes.append(componente)

        print("Número de componentes:", len(componentes))

        for i, componente in enumerate(componentes, 1):
            print(f"Componente {i}: {componente}")

    #funcao auxiliar de busca em profundidade adaptada para detectar ciclos
    def __bp_ciclo(self, vertice_atual, visitados, vertice_pai):
        visitados[vertice_atual] = True

        lista_vizinhos = self.vizinhos(vertice_atual + 1)

        for vizinho in lista_vizinhos:
            vizinho_index = vizinho - 1

            if visitados[vizinho_index] == False:
                if self.__bp_ciclo(vizinho_index, visitados, vertice_atual):
                    return True
                
            elif vizinho_index != vertice_pai:
                return True # encontrou ciclo
            
        return False

    #verifica se o grafo possui ciclo usando busca em profundidade
    def possui_ciclo(self):
        ordem = self.ordem()
        visitados = [False] * ordem

        for i in range(ordem):
            if(visitados[i] == False):
                if self.__bp_ciclo(i, visitados, -1):
                    return True
                
        return False
        
    #calcula o menor caminho de uma origem para todos os vertices usando dijkstra. devolve uma lista de tuplas no formato (vertice predecessor, distancia).
    def caminhos_minimos(self, vertice):
        origem_index = vertice - 1
        ordem = self.ordem()
        dt = [float('inf')] * ordem
        rot = [-1] * ordem
        rot[origem_index] = float('inf')
        dt[origem_index] = 0
        F = [False] * ordem
        A = [True] * ordem
        for _ in range(ordem):
            menor_dt = float('inf')
            r = -1
            for v in range(ordem):
                if (A[v] == True):
                    if (dt[v] < menor_dt):
                        menor_dt = dt[v]
                        r = v
            if r == -1:
                break
            F[r] = True
            A[r] = False
            V = []
            lista_vizinhos = self.vizinhos(r + 1)
            for i in lista_vizinhos:
                if (F[i - 1] == False):
                    V.append((i, self.matriz[r][i - 1]))   
            for i, peso in V:
                p = min(dt[i - 1], dt[r] + peso)
                if (p < dt[i - 1]):
                    dt[i - 1] = p
                    rot[i - 1] = r 
        resultado = []
        for v in range(ordem):
            #guardando o par (pai, distancia) para cada vertice
            if rot[v] != float('inf') and rot[v] != -1:
                rot_usuario = rot[v] + 1
            else:
                rot_usuario = float('inf')
            resultado.append((rot_usuario, dt[v]))
            
        return resultado

    #pega a distancia exata e a rota entre dois vertices. usa o resultado do menor_caminho e reconstroi o trajeto de tras pra frente usando os predecessores.
    def distancia_dois_vertices(self, origem, destino):
        resultado = self.caminhos_minimos(origem)

        destino_index = destino - 1
        predecessor, distancia = resultado[destino_index]
        caminho = []
        percorre = destino

        while percorre != origem:
            caminho.append(percorre)
            predecessor, _ = resultado[percorre - 1]

            if (predecessor == float('inf')):
                return float('inf'), []
            percorre = predecessor
        caminho.append(origem)
        caminho.reverse()

        return distancia, caminho


    # ------------------------------------------------------------------
    # TRABALHO 2 - CIRCUITO EULERIANO
    # ------------------------------------------------------------------

    #verifica se o grafo possui circuito euleriano. retorna (bool, motivo).
    #condicoes (grafo nao direcionado): 1) toda aresta esta em uma unica componente conexa
    #(vertices isolados sao ignorados) e 2) todos os vertices tem grau par.
    def possui_circuito_euleriano(self):
        n = self.ordem()

        #grafo sem arestas: nao ha circuito para apresentar
        if self.tamanho() == 0:
            return False, 'O grafo não possui arestas.'

        #condicao 2: todos os graus devem ser pares
        impares = [v for v in range(1, n + 1) if self.grau_vertice(v) % 2 != 0]
        if impares:
            return False, f'Existem vértices de grau ímpar: {impares}.'

        #condicao 1: todos os vertices com grau > 0 devem ser alcancados a partir de um deles
        com_aresta = [v for v in range(n) if any(self.matriz[v][u] != 0 for u in range(n))]
        visitado = [False] * n
        pilha = [com_aresta[0]]
        visitado[com_aresta[0]] = True

        while pilha:
            atual = pilha.pop()
            for u in range(n):
                if self.matriz[atual][u] != 0 and not visitado[u]:
                    visitado[u] = True
                    pilha.append(u)

        if not all(visitado[v] for v in com_aresta):
            return False, 'As arestas estão em mais de uma componente conexa.'

        return True, 'Todos os vértices têm grau par e as arestas estão em uma única componente.'

    #encontra um circuito euleriano com o algoritmo de Hierholzer (versao iterativa, sem recursao,
    #para suportar grafos de ate 1000 vertices). retorna a lista de vertices (base 1) do circuito,
    #comecando e terminando no mesmo vertice, ou None se o circuito nao existe.
    def circuito_euleriano(self, inicio=None):
        existe, _ = self.possui_circuito_euleriano()
        if not existe:
            return None

        n = self.ordem()

        #copia das listas de adjacencia (as arestas serao removidas conforme usadas)
        adj = [set(u for u in range(n) if self.matriz[v][u] != 0) for v in range(n)]

        if inicio is None:
            inicio = next(v for v in range(n) if adj[v])
        else:
            inicio -= 1
            if not adj[inicio]:
                return None #vertice sem arestas nao pode iniciar o circuito

        pilha = [inicio]
        circuito = []

        while pilha:
            v = pilha[-1]
            if adj[v]:
                u = adj[v].pop() #usa a aresta (v,u)
                adj[u].remove(v) #remove a mesma aresta no outro sentido
                pilha.append(u)
            else:
                circuito.append(pilha.pop()) #vertice sem arestas livres entra no circuito

        circuito.reverse()
        return [v + 1 for v in circuito]

    #soma o peso das arestas percorridas por um circuito (util para exibir o custo total)
    def custo_circuito(self, circuito):
        return sum(self.matriz[a - 1][b - 1] for a, b in zip(circuito, circuito[1:]))

    def arvore_geradora_minima(self):
        n = self.ordem()

        #junta cada aresta uma unica vez (so o triangulo superior da matriz); peso 0 significa que nao ha aresta
        todas_arestas = [(self.matriz[i][j], i, j)
                         for i in range(n)
                         for j in range(i + 1, n)
                         if self.matriz[i][j] != 0]
        todas_arestas.sort() #ordena por peso e, em caso de empate, por (i, j)

        #union-find: cada vertice comeca sozinho no proprio conjunto
        pai = list(range(n))
        tamanho = [1] * n

        #acha o representante do conjunto do vertice v, ja achatando o caminho percorrido
        def representante(v):
            raiz = v
            while pai[raiz] != raiz:
                raiz = pai[raiz]

            while pai[v] != raiz:
                proximo = pai[v]
                pai[v] = raiz
                v = proximo

            return raiz

        arestas_agm = []
        custo_total = 0

        for peso, i, j in todas_arestas:
            raiz_i = representante(i)
            raiz_j = representante(j)

            #mesmo conjunto: a aresta fecharia um ciclo, entao e descartada
            if raiz_i == raiz_j:
                continue

            #une os dois conjuntos (o menor passa a apontar para o maior)
            if tamanho[raiz_i] < tamanho[raiz_j]:
                raiz_i, raiz_j = raiz_j, raiz_i
            pai[raiz_j] = raiz_i
            tamanho[raiz_i] += tamanho[raiz_j]

            arestas_agm.append((i + 1, j + 1, peso))
            custo_total += peso

            #uma arvore geradora tem exatamente n - 1 arestas, entao nao precisa olhar o resto
            if len(arestas_agm) == n - 1:
                break

        #se faltaram arestas para ligar todos os vertices, o grafo nao e conexo
        if len(arestas_agm) != n - 1:
            return None

        return arestas_agm, custo_total


    # MÉTRICAS DE DISTÂNCIA
    def excentricidade(self, vertice):
        resultados = self.caminhos_minimos(vertice)

        # Filtra as distâncias, ignorando a distância para ele mesmo e vértices inalcançáveis
        distancias = [dist for _, dist in resultados if dist > 0 and dist != float('inf')]
        
        if not distancias:
            return 0            
        return max(distancias)

    def metricas_distancia(self):
        n = self.ordem()
        
        # Checa se o grafo é conexo antes de calcular tudo
        # Se alguma distância a partir do vértice 1 for infinita, tem vértice isolado
        resultados_v1 = self.caminhos_minimos(1)
        if any(dist == float('inf') for _, dist in resultados_v1):
            return None # Avisa o main.py que o grafo é desconexo

        excentricidades = {}
        for v in range(1, n + 1):
            excentricidades[v] = self.excentricidade(v)
            
        raio = min(excentricidades.values())
        diametro = max(excentricidades.values())
        
        vertices_min = [v for v, exc in excentricidades.items() if math.isclose(exc, raio)]
        vertices_max = [v for v, exc in excentricidades.items() if math.isclose(exc, diametro)]
        
        return excentricidades, raio, diametro, vertices_min, vertices_max
