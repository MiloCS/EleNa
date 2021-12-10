import networkx
from networkx import single_source_dijkstra as ssd
from heapq import *

class Router:
    def __init__(self, g):
        self.g = g

    def get_route(self, start, end, max_length):
        pass

    def elevation_diff(self, nodeNumA, nodeNumB, edge_attrs):
        nodeA, nodeB = self.g.nodes()[nodeNumA], self.g.nodes()[nodeNumB] 
        return abs(nodeA['elevation'] - nodeB['elevation'])

    def get_path_length(self, path, elevation=False):
        g = self.g
        total = 0
        for i in range(len(path) - 1):
            if elevation:
                total += self.elevation_diff(path[i], path[i+1], None)
            else:
                total += g[path[i]][path[i+1]][0]['length']
        return total

    def modified_dijkstra(self, start, end, cutoff, max_bool):
        G = self.g
        Gs = G._succ

        prev = {}
        seen = {}

        elev = {}
        dist = {}

        seen[start] = 0

        frontier = []
        heappush(frontier, (0, 0, start)) #elevation, distance, vertex

        while frontier:
            e, d, v = heappop(frontier)
            if v in elev:
                continue
            
            elev[v] = e
            dist[v] = d
            if v == end:
                break
            
            for u, e in Gs[v].items():
                
                distcost = e[0]['length']
                elcost = self.elevation_diff(u, v, e)

                exten_dist = dist[v] + distcost
                exten_elev = elev[v] + elcost
                if exten_dist > cutoff:
                    continue
                if u not in seen or exten_elev < seen[u]:
                    seen[u] = exten_elev
                    if max_bool:
                        exten_elev = -1 * exten_elev
                    heappush(frontier, (exten_elev, exten_dist, u))
                    prev[u] = v
        
        path = []
        curr = end
        path.append(curr)
        while curr != start:
            #print(curr)
            curr = prev[curr]
            path.append(curr)
        return list(reversed(path))


class MinRouter(Router):
    def __init__(self, g):
        super().__init__(g)
    
    def get_route(self, start, end, max_length):
        try:
            path = self.modified_dijkstra(start, end, max_length, False)
        except Exception as e:
            print(e)
            path = ssd(self.g, start, end, weight='length')[1]
        return path, self.get_path_length(path), self.get_path_length(path, elevation=True)


class MaxRouter(Router):
    def __init__(self, g, dfs=False):
        super().__init__(g)
        self.use_dfs = dfs

    def get_route(self, start, end, max_length):
        if self.use_dfs:
            func = self.simple_paths_cost
        else:
            func = self.modified_dijkstra
        try:
            path = func(start, end, max_length, True)
        except Exception as e:
            print(e)
            path = ssd(self.g, start, end, weight='length')[1]
        return path, self.get_path_length(path), self.get_path_length(path, elevation=True)
    
    def simple_paths_cost(self, start, end, max_length, max):
        G = self.g
        visited = dict.fromkeys([source])
        stack = [(v for u, v in G.edges(source))]
        while stack:
            children = stack[-1]
            child = next(children, None)
            if child is None:
                stack.pop()
                visited.popitem()
            elif self.get_path_length(G, visited) <= cutoff:
                if child in visited:
                    continue
                if child in targets:
                    yield list(visited) + [child]
                visited[child] = None
                if targets - set(visited.keys()):
                    stack.append((v for u, v in G.edges(child)))
                else:
                    visited.popitem()
            else:
                stack.pop()
                visited.popitem()