'''
@inproceedings{nr,
     title={The Network Data Repository with Interactive Graph Analytics and Visualization},
     author={Ryan A. Rossi and Nesreen K. Ahmed},
     booktitle={AAAI},
     url={https://networkrepository.com},
     year={2015}
}
'''

from data_structure.graph import Graph
from functools import reduce
from tabulate import tabulate

class Airport:
    @staticmethod
    def load_vertex():
        with open('data\\USAir97_nodename.txt', 'r', encoding='utf-8') as file:
            for airport in file:
                airport = airport.replace('\n', '')
                graph.create_vertex(airport)        
    
    @staticmethod
    def load_edge():
        with open('data\\USAir97.txt', 'r', encoding='utf-8') as file:
            for edge in file:
                if '%' not in edge:
                    edge = edge.replace('\n', '')
                    v1, v2, w = edge.split(' ')
                    graph.create_edge(int(v1), int(v2), float(w)) if v1 != v2 else None
    
    @staticmethod
    def all_airports_details():
        data = []
        headers = ['ID', 'NAME', 'EDGES COUNT']
        for vertex in range(1, graph.num_vertex_+1):
            vertex_detail = graph.get_vertex_detail(vertex)
            data.append([vertex_detail['id'], vertex_detail['name'], vertex_detail['num_edges']])
        
        return tabulate(data, headers = headers, tablefmt="github")
    
    @staticmethod
    def airport_detail(vertex):
        res = graph.get_vertex_detail(vertex)
        data = [  ['ID', res['id']]
                , ['NAME', res['name']]
                , ['EDGES QUANTITY', res['num_edges']]
                , ['EDGES', res['edges']]]
        
        return tabulate(data, tablefmt= 'github')
    
    @staticmethod
    def fit_dijkstra(vertex_initial, debug = False):
        graph.fit_dijkstra(vertex_initial, debug)
    
    @staticmethod
    def disjkstra_result(vertex, min_layover = 0, max_layover = 10**6, mode = 'one'):
        res = graph.dijkstra_result(vertex)
        if not res:
            return tabulate(['DIJKSTRA NOT FITTING'], tablefmt="github")
        
        if mode == 'one':
            data = list()
            for i, airport in enumerate(res['route'], start = 1):
                data.append([i,  airport])
            data.append(['MILES', round(res['cost'], 3)])
            
            return tabulate(data, headers=['LAYOVER', 'AIRPORT'], tablefmt="github")
    
        elif mode == 'all':
            layover, cost = len(res['route']), round(res['cost'], 3)
            return [layover, cost] if layover in range(min_layover, max_layover+1) else None
    
    @staticmethod
    def data_credits():
        headers = ['TITLE', 'AUTHOR', 'BOOKTITLE', 'URL', 'YEAR']
        data = [['The Network Data Repository with Interactive Graph Analytics and Visualization'
                 , 'Ryan A. Rossi and Nesreen K. Ahmed'
                 , 'AAAI'
                 , 'https://networkrepository.com'
                 , 2015]]
        
        return tabulate(data, headers, tablefmt="github")

    
    
graph = Graph(directed=False, weighted=True, start_with=1)

Airport.load_vertex()
Airport.load_edge()

print(tabulate([['VERTEX QUANTITY', graph.num_vertex_]
             , ['EDGES QUANTITY', graph.num_edges_]]
    ))

if __name__ == '__main__':   
    data = [  [1, 'ALL AIRPORTS DETAILS']
            , [2, 'AIRPORT DETAIL']
            , [3, 'FIT DIJKSTRA']
            , [4, 'AIRPORT ROUTE']
            , [5, 'MAP ALL ROUTES']
            , [6, 'DATA CREDITS']
            , [7, 'EXIT']
            ]
    headers = ["SELECT", "OPTION"]
    vertex_initial = None
    op = None
    
    while op != '7':
        print(tabulate(data, headers = headers, tablefmt="grid"))
        op = input('\n>> ')

        if op == '1':
            print(Airport.all_airports_details(), end='\n\n')
        
        elif op == '2':
            vertex = int(input('Airport ID \n>> '))
            print(Airport.airport_detail(vertex), end='\n\n')

        elif op == '3':
            vertex_initial = int(input('Initial Airport ID \n>> '))

        elif op == '4':
            vertex = int(input('Airport ID \n>> '))
            try:
                print(f'ROUTES FROM AIRPORT {graph.vertex[vertex_initial]} TO AIRPORT {graph.vertex[vertex]}')
            except:
                pass
            print(Airport.disjkstra_result(vertex, mode = 'one'), end='\n\n')

        elif op == '5':
            min_layover, max_layover = 0, 10**6
            min_l = input('Minimum number of layovers (optional)\n>> ')
            max_l = input('Maximum number of layovers (optional)\n>> ')
            min_layover = int(min_l) if min_l else min_layover
            max_layover = int(max_l) if max_l else max_layover

            count_results = 0
            greater_distance = (None, None, 0)

            for id_src, source in graph.vertex.items():
                targets = list()
                
                Airport.fit_dijkstra(id_src)
                for id_trg, target in graph.vertex.items():
                    if id_src != id_trg:
                        res = Airport.disjkstra_result(id_trg, min_layover, max_layover, mode = 'all') 
                        targets.append([target]+res) if res else None
                
                if targets:
                    count_results += len(targets)
                    greater_distance_vertex = reduce(lambda x, y: x if x[2] > y[2] else y, targets, (None, None, 0))
                    greater_distance_vertex = (source, greater_distance_vertex[0], greater_distance_vertex[2])

                    if greater_distance_vertex[2] > greater_distance[2]:
                        greater_distance = greater_distance_vertex

                    print(tabulate([[f'ROUTES FROM THE AIRPORT: {source}']], tablefmt="github"))
                    print(tabulate(targets, headers=['TARGET', 'LAYOVER QUANTITY', 'MILES'], tablefmt='github'), end='\n\n')
            print(f'{count_results} ROUTES FOUND')
            print(f'GREATER DISTANCE\nSOURCE: {greater_distance[0]}\nTARGET: {greater_distance[1]}\n{greater_distance[2]}')

        elif op == '6':
            print(Airport.data_credits(), end='\n\n')
        
