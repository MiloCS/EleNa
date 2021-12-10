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
    
    def neg_elevation_diff(self, nodeA, nodeB, edge_attrs):
        return -1 * self.elevation_diff(nodeA, nodeB, edge_attrs)


class MinRouter(Router):
    def __init__(self, g):
        super().__init__(g)
    
    def get_route(self, start, end, max_length):
        path = self.modified_dijkstra(start, end, max_length)
        #path = ssd(self.g, start, end, weight=self.elevation_diff)[1]
        return path, get_path_length(self.g, path), get_path_length(self.g, path, elevation=True)

    def modified_dijkstra(self, source, target, cutoff):
        G = self.g
        Gs = G._succ

        prev = {}
        seen = {}
        elev = {}
        dist = {}

        seen[source] = 0

        frontier = []
        heappush(frontier, (0, 0, source)) #elevation, distance, vertex

        while frontier:
            e, d, v = heappop(frontier)
            if v in elev:
                #print("continuing", len(frontier))
                continue
            
            elev[v] = e
            dist[v] = d
            #print(d)
            if v == target:
                #print("breaking")
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
                    heappush(frontier, (exten_elev, exten_dist, u))
                    prev[u] = v
        
        path = []
        curr = target
        path.append(curr)
        while curr != source:
            #print(curr)
            curr = prev[curr]
            path.append(curr)
        return list(reversed(path))

class MaxRouter(Router):
    def __init__(self, g):
        super().__init__(g)

    def get_route(self, start, end, max_length):
        #return ssbf(self.g, start, end, weight=self.neg_elevation_diff)
        print(self.targeted_dfs(start, end, max_length))
        # p = networkx.all_simple_paths(self.g, start, end, cutoff=10)
        # print(next(p))
        path = ssd(self.g, start, end, weight='length')[1]
        return path, get_path_length(self.g, path), get_path_length(self.g, path, elevation=True)
        #return get_max_path(self.g, start, end, percent, max_length)

    def targeted_dfs(self, source, target, cutoff):
        G = self.g
        path_visited = set()
        stack = [(source, 0, iter(G[source]))]
        paths = []
        while stack:
            current, dist_to_node, children = stack[-1]
            try:
                child = next(children)
                if child not in path_visited:
                    dst = G[current][child][0]['length']
                    if child == target:
                        stack.append((child, dist_to_node + dst, iter(G[child])))
                        paths.append(stack)
                        stack.pop()
                    else:
                        if dist_to_node + dst < cutoff:
                            path_visited.add(child)
                            stack.append((child, dist_to_node + dst, iter(G[child])))
            except StopIteration:
                node = stack.pop()
                print(path_visited)
                path_visited.remove(node[0])
        return paths

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