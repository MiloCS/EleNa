from networkx import single_source_dijkstra as ssd

class Router:
    def __init__(g):
        self.g = g
        self.max_length

    def get_route(start, end, max_length):
        pass

class MinRouter(Router):
    def __init__(g, algo="dijkstra"):
        super(g)
        self.algo = algo
    
    def get_route(start, end, max_length):
        return ssd(self.g, start, end)

class MaxRouter(Router):
    def __init__(g, algo="dijkstra"):
        super(g)
        self.algo = algo

    def get_route(start, end, max_length):
        pass