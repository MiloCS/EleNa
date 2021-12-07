from networkx import single_source_dijkstra as ssd
from networkx import single_source_bellman_ford as ssbf

class Router:
    def __init__(self, g):
        self.g = g

    def get_route(self, start, end, max_length):
        pass

    def elevation_diff(self, nodeNumA, nodeNumB, edge_attrs):
        nodeA, nodeB = self.g.nodes()[nodeNumA], self.g.nodes()[nodeNumB] 
        return abs(nodeA['elevation'] - nodeB['elevation'])
    
    def neg_elevation_diff(self, nodeA, nodeB, edge_attrs):
        return -1 * elevation_diff(nodeA, nodeB, edge_attrs)


class MinRouter(Router):
    def __init__(self, g, algo="dijkstra"):
        super().__init__(g)
        self.algo = algo
    
    def get_route(self, start, end, max_length):
        return ssd(self.g, start, end, weight=self.elevation_diff)

class MaxRouter(Router):
    def __init__(self, g, algo="dijkstra"):
        super().__init__(g)
        self.algo = algo

    def get_route(self, start, end, max_length):
        return ssbf(self.g, start, end, weight=self.neg_elevation_diff)