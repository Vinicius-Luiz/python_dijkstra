## Autor: Vinícius Luiz
## LinkedIn: linkedin.com/in/vlsf2/
## Copyright(c) 2023 Vinícius Luiz da Silva França


# #1 - Contexto do Problema

Em 1997, havia 332 aeroportos no Estados Unidos, com isso, seria possível conter cerca de 54.946 rotas sem escala no território americano. Porém, das 54.946 rotas sem escalas possíveis, somente 2126 eram utilizadas, ou seja, 96% das rotas possíveis não existiam.  
***Para R = Rota; A = Aeroporto 1; B Aeroporto 2: R(A|B) = R(B|A)***

# #2 - Desafio

Encontrar a **menor rota** entre dois aeroportos não conectados.

# #3 - Base de dados

A base de dados “Pajek network: US Air flights, 1997” contém 3 arquivos:
### USAir97
Considerando vertices = aeroportos e arestas = rotas:
- quantidade de aeroportos
- quantidade de rotas
- rotas (aeroporto_A, aeroporto_B, distância_em_milhas)

O grafo é **ponderado** e **não direcionado**
### USAir97_nodename
- Nome dos aeroportos
### USAir97_coord
- Coordenada dos aeroportos


# #4 - Solução
## Class Vertex
```python
class Vertex():
    def __init__(self, name: str, id: int) -> None:
        self.id = id
        self.name = name
        self.edges = dict()
```

## Class Graph
```python
class Graph():
    INF = 999

    def __init__(self, directed: bool = False, weighted: bool = False, start_with: int = 1, num_vertex: int = 9999) -> None:
        self.directed = directed
        self.weighted = weighted
        self.vertex = dict()
        self.sequence = iter(range(start_with, num_vertex))

        self.num_vertex_ = 0
        self.num_edges_ = 0

        # dijkstra
        self.dijkstra_queue = list() # [(weight, vertex_id)]
        self.dijkstra_results = dict()
```

## Algoritmo de Dijkstra
O algoritmo de Dijkstra é um algoritmo de caminho mínimo para encontrar o caminho mais curto entre dois nós em um grafo com pesos não negativos. Ele foi desenvolvido por Edsger W. Dijkstra em 1956.  

O algoritmo usa uma abordagem "vai e vem" para visitar todos os nós no grafo, mantendo sempre o caminho mais curto conhecido até cada nó. Ele inicia no nó de origem e, a cada iteração, seleciona o nó com a menor distância conhecida até o momento e atualiza as distâncias para seus vizinhos. Este processo continua até que se chegue ao nó de destino.  

Referências:

- Dijkstra, Edsger W. "A note on two problems in connexion with graphs." Numerische Mathematik 1.1 (1959): 269-271.
- https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm

A implementação do algoritmo de Dijkstra foi inspirada na resolução da plataforma https://visualgo.net/en.  
Visualgo.net é uma plataforma educacional on-line que oferece animações interativas e recursos visuais para ajudar a entender conceitos de algoritmos e estruturas de dados de computação, como árvores, grafos, ordenação e busca. É uma ferramenta útil para estudantes, professores e programadores que desejam melhorar suas habilidades e compreender melhor esses conceitos.

### Limitação do algoritmo de Dijkstra para grafos não-direcionados
O Algoritmo de Dijkstra é projetado para trabalhar com grafos com pesos positivos em que as arestas têm direção, ou seja, são grafos direcionados. Se um grafo for não direcionado, a distância mínima entre dois vértices pode ser diferente dependendo do caminho que você escolher. Além disso, o Algoritmo de Dijkstra não funciona para grafos com arestas de peso negativo, pois o resultado não garante a existência de um caminho mínimo.  

### Exemplo de mal funcionamento:  
Neste caso, note que determinado aeroporto **(248) Los Angeles Intl** se repete para o aeroporto **(146) La Gardia**. Além da repetição, após separar as rotas que não se repetem, é possível notar que elas foram calculadas em ordem decrescente (da maior rota para a menor). Este case se repete para outros casos que possuem o mesmo mal funcionamento.  

**ROUTES FROM AIRPORT (248) Los Angeles Intl TO AIRPORT (146) La Guardia**

| LAYOVER   | AIRPORT                              |
| --------- | ------------------------------------ |
| 1         | **(248) Los Angeles Intl**           |
| 2         | (168) Eagle County Regional          |
| 3         | **(248) Los Angeles Intl**           |
| 4         | (166) Stapleton Intl                 |
| 5         | **(248) Los Angeles Intl**           |
| 6         | (172) Kansas City Intl               |
| 7         | **(248) Los Angeles Intl**           |
| 8         | (182) Lambert-St Louis Intl          |
| 9         | **(248) Los Angeles Intl**           |
| 10        | (176) Cincinnati/Northern Kentucky I |
| **MILES** | **0.236**                            |

#### Separando as rotas para determinar a rota de menor percurso

| LAYOVER   | AIRPORT                              |
|-----------|--------------------------------------|
| 1         | (248) Los Angeles Intl               |
| 2         | (168) Eagle County Regional          |
R(248/168) + R(168/146) = 0,080 + 0,169 = 0,249

| LAYOVER   | AIRPORT                              |
|-----------|--------------------------------------|
| 3         | (248) Los Angeles Intl               |
| 4         | (166) Stapleton Intl                 |
R(248/166) + R(166/146) = 0,089 + 0,158 = 0,247

| LAYOVER   | AIRPORT                              |
|-----------|--------------------------------------|
| 5         | (248) Los Angeles Intl               |
| 6         | (172) Kansas City Intl               |
R(248/172) + R(172/146) = 0,131 + 0,107 = 0,238

| LAYOVER   | AIRPORT                              |
|-----------|--------------------------------------|
| 7         | (248) Los Angeles Intl               |
| 8         | (182) Lambert-St Louis Intl          |
R(248/182) + R(182/146) = 0,150 + 0,086 = **0,236**

| LAYOVER   | AIRPORT                              |
|-----------|--------------------------------------|
| 9         | (248) Los Angeles Intl               |
| 10        | (176) Cincinnati/Northern Kentucky I |
R(276/176) + R(176/146) = 0,179 + 0,057 = **0,236**

#### Solução do mal funcionamento
A solução proposta é retornar a última rota que não se repete que o algoritmo de Dijkstra armazena.

**ROUTES FROM AIRPORT (248) Los Angeles Intl TO AIRPORT (146) La Guardia**

| LAYOVER   | AIRPORT                              |
|-----------|--------------------------------------|
| 1         | (248) Los Angeles Intl               |
| 2         | (176) Cincinnati/Northern Kentucky I |
| MILES     | 0.236                                |

# #5 - Resultados encontrados

## Eficácia
Em uma busca completa das 54.946 rotas possíveis, o algoritmo de Dijkstra encontrou uma rota ótima para **todas elas**, ou seja, para todo Aeroporto A, conseguimos chegar a qualquer outro Aeroporto B através do algoritmo.

## Quantidade de escalas
- **30.237 voos** com 2 escalas
- **45.915 voos** com 3 escalas
- **22.319 voos** com 4 escalas
- **6650 voos** com 5 escalas
- **972 voos** com 6 escalas
- **102 voos** com 7 escalas
- **2 voos** com 8 escalas

**ROUTES FROM AIRPORT (281) Mobile Regional TO AIRPORT (48) Pangborn Memorial**
| LAYOVER   | AIRPORT                             |
|-----------|-------------------------------------|
| 1         | (281) Mobile Regional               |
| 2         | (286) Pensacola Regional            |
| 3         | (284) Jacksonville Intl             |
| 4         | (118) Chicago O'hare Intl           |
| 5         | (83) Boise Air Terminal /Gowen Fld/ |
| 6         | (58) Lewiston-Nez Perce County      |
| 7         | (60) Walla Walla Regional           |
| 8         | (49) Grant County                   |
| MILES     | 0.242                               |

**ROUTES FROM AIRPORT (320) Rafael Hernandez TO AIRPORT (48) Pangborn Memorial**
| LAYOVER   | AIRPORT                             |
|-----------|-------------------------------------|
| 1         | (320) Rafael Hernandez              |
| 2         | (324) Mercedita                     |
| 3         | (321) Luis Munoz Marin Intl         |
| 4         | (118) Chicago O'hare Intl           |
| 5         | (83) Boise Air Terminal /Gowen Fld/ |
| 6         | (58) Lewiston-Nez Perce County      |
| 7         | (60) Walla Walla Regional           |
| 8         | (49) Grant County                   |
| MILES     | 0.398                               |

## Maior distância
Após realizar a busca das 54.946 rotas, o voo entre **(37) Eareckson As** e **(330) West Tinian** possui a maior distância em milhas: **0.962**

**ROUTES FROM AIRPORT (37) Eareckson As TO AIRPORT (330) Babelthuap/Koror**
| LAYOVER   | AIRPORT             |
|-----------|---------------------|
| 1         | (37) Eareckson As   |
| 2         | (8) Anchorage Intl  |
| 3         | (313) Honolulu Intl |
| 4         | (329) Guam Intll    |
| MILES     | 0.962               |

# #5 - Conclusão
- Desde que todas as rotas existentes estejam bem distribuídas, conseguimos suprir a necessidade das rotas faltantes.
- O algoritmo de Dijkstra mostra grande eficiência quando se trata de rotas aéreas, visto que um país como o Estados Unidos possui aeroportos bem distribuídos em seu território.
- E quanto aos voos com muitas escalas? Dependendo da demanda dessa rota, é viável criar novas rotas para diminuir as escalas desse voo.