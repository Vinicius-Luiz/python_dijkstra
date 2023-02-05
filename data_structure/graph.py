# vinicius.luiz
# https://www.linkedin.com/in/vlsf2/
# 03/02/2023

from data_structure.vertex import Vertex
from typing import List, Tuple

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

    def __str__(self) -> str:
        output = str()
        for v in self.vertex.values():
            output += f'{v}\n'
        
        return output

    def _get_next_sequence(self) -> int:
        return next(self.sequence)
    
    def _get_routes(self, routes: List[Tuple[int, int]], vertex_initial: int):
        for source, target in routes[::-1]:
            current_source = source
            while True:
                self.dijkstra_results[target]['route'].insert(0, self.vertex[current_source])
                if vertex_initial != current_source:
                    current_source = list(filter(lambda x: x[1] == current_source, routes))[0][0]
                else:
                    break

    def get_vertex_detail(self, vertex_id: int) -> dict:
        new_dict = dict()
        try:
            vertex = self.vertex[vertex_id]
        except:
            return None
        
        new_dict['id'] = vertex.get_id()
        new_dict['name'] = vertex.get_name()
        new_dict['num_edges'] = vertex.get_num_edges()
        new_dict['edges'] = vertex.get_edges()

        return new_dict    

    def get_edges(self, vertex_id: int) -> dict:
        return self.vertex[vertex_id].get_edges()
    
    def create_vertex(self, name: str) -> None:
        new_id = self._get_next_sequence()
        self.vertex[new_id] = Vertex(name, new_id)

        self.num_vertex_ += 1

    def create_edge(self, v1: int, v2: int, weight: int = None):
        if self.weighted and not weight:
            raise Exception('The edge must contain a weight')
        
        res = self.vertex[v1].set_edge(v2, weight)
        if not self.directed:
            self.vertex[v2].set_edge(v1, weight)
        
        if res:
            self.num_edges_ += 1
    
    def delete_vertex(self, id: int) -> None:
        if self.vertex.pop(id, None):
            self.num_vertex_ -= 1
    
    def delete_edge(self, v1: int, v2: int) -> None:
        if self.vertex[v1].edges.pop(v2):
            self.num_edges_ -= 1

    def fit_dijkstra(self, vertex_initial: int, debug = False) -> None:
        if not self.weighted:
            raise Exception('The graph must be weighted')

        print(f'{vertex_initial} is the source vertex\n') if debug else None
        self.dijkstra_queue.clear()
        self.dijkstra_results.clear()
        routes = list()

        self.dijkstra_queue.append((0, vertex_initial))
        for id in self.vertex.keys():
            if id != vertex_initial:
                self.dijkstra_queue.append((self.INF, id))
            self.dijkstra_results[id] = {'cost': self.INF, 'route': list()}
        
        
        while self.dijkstra_queue:
            current_weight, current_vertex = self.dijkstra_queue[0][0], self.dijkstra_queue[0][1]
            print(f'The current priority queue {self.dijkstra_queue}') if debug else None
            print(f'Exploring neighbors of vertex u = {current_vertex}, d[u] = {current_weight}') if debug else None
            temp_weights = dict()
            self.dijkstra_queue.pop(0)
            
            vertex_edges = self.get_edges(current_vertex)
            for edge_vertex, edge_weight in vertex_edges.items():
                temp_weights[edge_vertex] = current_weight + edge_weight
                print(f'd[{edge_vertex}] = d[{current_vertex}] + w({current_vertex}, {edge_vertex}) = {current_weight}+{edge_weight} = {current_weight+edge_weight}, p[{edge_vertex}] = {current_vertex}') if debug else None

                weight_vertex_queue = self.dijkstra_results[edge_vertex]['cost']
                if current_weight+edge_weight <= weight_vertex_queue:
                    self.dijkstra_queue = list(filter(lambda x: x[1] != edge_vertex, self.dijkstra_queue))
                    self.dijkstra_queue.append((temp_weights[edge_vertex], edge_vertex))

                    self.dijkstra_results[edge_vertex]['cost'] = temp_weights[edge_vertex]
                    
                    routes.append((current_vertex, edge_vertex))
                else:
                    print(f'd[{current_vertex}] + w({current_vertex}, {edge_vertex}), i.e {current_weight}+{edge_weight} > {weight_vertex_queue}, so there is no change.') if debug else None
                
                self.dijkstra_queue = sorted(self.dijkstra_queue, key=lambda x: x[0])
            print(f'd[{current_vertex}]: {current_weight} is final as all outgoing edges of this vertex has been processed.\n\n') if debug else None

        self._get_routes(routes, vertex_initial)
    
    def dijkstra_result(self, vertex: int) -> int:
        res = self.dijkstra_results.get(vertex) 

        if not res or res['cost'] == self.INF:
            return None
        
        if len(res['route']) != len(set(res['route'])):
            first_vertex = res['route'][0]
            route_reverse = res['route'][::-1]
            index_reverse = route_reverse.index(first_vertex)
            res['route'] = res['route'][len(res['route'])-index_reverse-1:]
        
        return res
    
if __name__ == '__main__':
    pass