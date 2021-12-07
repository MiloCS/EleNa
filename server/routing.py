from networkx import single_source_dijkstra as ssd
from networkx import single_source_bellman_ford as ssbf
from heapq import *

class Router:
    def __init__(self, g):
        self.g = g

    def get_route(self, start, end, max_length, percent):
        pass

    def elevation_diff(self, nodeNumA, nodeNumB, edge_attrs):
        nodeA, nodeB = self.g.nodes()[nodeNumA], self.g.nodes()[nodeNumB] 
        return abs(nodeA['elevation'] - nodeB['elevation'])
    
    def neg_elevation_diff(self, nodeA, nodeB, edge_attrs):
        return -1 * self.elevation_diff(nodeA, nodeB, edge_attrs)


class MinRouter(Router):
    def __init__(self, g, algo="dijkstra"):
        super().__init__(g)
        self.algo = algo
    
    def get_route(self, start, end, max_length, percent):
        path = ssd(self.g, start, end, weight=self.elevation_diff)[1]
        print(path)
        return path, get_path_length(self.g, path), get_path_length(self.g, path, elevation=True)

class MaxRouter(Router):
    def __init__(self, g):
        super().__init__(g)

    def get_route(self, start, end, max_length, percent):
        #return ssbf(self.g, start, end, weight=self.neg_elevation_diff)
        return get_max_path(self.g, start, end, percent, max_length)

def elevation_diff(g, nodeNumA, nodeNumB, edge_attrs):
        nodeA, nodeB = g.nodes()[nodeNumA], g.nodes()[nodeNumB] 
        return abs(nodeA['elevation'] - nodeB['elevation'])

def get_path_length(g, path, elevation=False):
    #path = #list(path.keys())
    total = 0
    for i in range(len(path) - 1):
        if elevation:
            total += elevation_diff(g, path[i], path[i+1], None)
        else:
            total += g[path[i]][path[i+1]][0]['length']
    return total

#heavily adapted from networkx.all_simple_paths()
def simple_paths_cost(G, source, target, cutoff):
    visited = dict.fromkeys([source])
    stack = [(v for u, v in G.edges(source))]
    while stack:
        children = stack[-1]
        child = next(children, None)
        if child is None:
            stack.pop()
            visited.popitem()
        elif get_path_length(G, visited) <= cutoff:
            if child in visited:
                continue
            if child is target:
                yield list(visited) + [child]
            visited[child] = None
            if target not in set(visited.keys()):
                stack.append((v for u, v in G.edges(child)))
            else:
                visited.popitem()
        else:  # len(visited) == cutoff:
            # for target in targets - set(visited.keys()):
            #     count = ([child] + list(children)).count(target)
            #     for i in range(count):
            #         yield list(visited) + [target]
            stack.pop()
            visited.popitem()