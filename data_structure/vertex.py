class Vertex():
    def __init__(self, name: str, id: int) -> None:
        self.id = id
        self.name = name
        self.edges = dict()

    def __str__(self) -> str:
        return f'({self.id}) {self.name}'

    def get_id(self) -> int:
        return self.id
    
    def get_name(self) -> str:
        return self.name
    
    def get_num_edges(self) -> int:
        return len(self.edges)
    
    def get_edges(self) -> dict:
        return self.edges
    
    def set_edge(self, v2: int, weight: int) -> bool:
        if v2 not in self.edges:
            self.edges[v2] = weight
            return True
        return False