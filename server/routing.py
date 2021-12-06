from networkx import single_source_dijkstra as ssd

class Router:
    def __init__(self, g):
        self.g = g

    def get_route(self, start, end, max_length):
        pass

class MinRouter(Router):
    def __init__(self, g, algo="dijkstra"):
        super().__init__(g)
        self.algo = algo
    
    def get_route(self, start, end, max_length):
        return ssd(self.g, start, end, cutoff=max_length)

class MaxRouter(Router):
    def __init__(self, g, algo="dijkstra"):
        super().__init__(g)
        self.algo = algo

    def get_route(self, start, end, max_length):
        pass