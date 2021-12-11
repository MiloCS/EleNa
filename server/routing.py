"""
A module that defines the different types of routing available for EleNa.
The PathFinder class in index.py uses a strategy pattern with the classes in this module.

      Router
      /   \\
MinRouter  MaxRouter

Most of the code in this module defines the algorithms for min/maxing elevation.
"""

import networkx
from networkx import single_source_dijkstra as ssd
from heapq import *

class Router:
    """
    a generic Router class that is the superclass for the other classes in this module
    """
    def __init__(self, g):
        """
        initializes Router object with a networkx graph instance variable
        :param g: networkx graph
        """
        self.g = g

    def get_route(self, start, end, max_length):
        """
        template method for the get_route function in this class's subclasses
        :param start: node number for start node
        :param end: node number for end node
        :param max_length: maximum length of path generated
        """
        pass

    def elevation_diff(self, nodeNumA, nodeNumB, edge_attrs):
        """
        utility function for getting the elevation difference between 2 nodes in the graph
        :param nodeNumA: first node number in graph
        :param nodeNumB: second node number in graph
        :param edge_attrs: edge attributes - not used in this context, included for compatibility with networkx
        :return: elevation difference
        """
        nodeA, nodeB = self.g.nodes()[nodeNumA], self.g.nodes()[nodeNumB] 
        return abs(nodeA['elevation'] - nodeB['elevation'])

    def get_path_length(self, path, elevation=False):
        """
        given a list of path nodes, uses graph to find total length or elevation change along path
        :param path: list of path node numbers
        :param elevation: whether function should get elevation difference instead of distance length
        :return: length or elevation change of path
        """
        g = self.g
        total = 0
        for i in range(len(path) - 1):
            if elevation:
                total += self.elevation_diff(path[i], path[i+1], None)
            else:
                total += g[path[i]][path[i+1]][0]['length']
        return total

    def modified_dijkstra(self, start, end, cutoff, max_bool):
        """
        performs a modified version of dijkstra's algorithm, trying to min/max elevation
        also keeps track of path distance so it can cutoff the algorithm if paths go past that

        heavily adapted from the networkx implementation of dijkstra's algorithm
        :param start: start node num
        :param end: end node num
        :param cutoff: max path length
        :param max_bool: whether or not to maximize elevation
        :return: path list of node nums
        """
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
    """
    A Router template for minimizing path elevation
    """
    def __init__(self, g):
        """
        initializes a MinRouter
        :param g: networkx graph
        """
        super().__init__(g)
    
    def get_route(self, start, end, max_length):
        """
        gets route, minimizing elevation gain, constrained by the max distance given
        :param start: node number for start node
        :param end: node number for end node
        :param max_length: maximum length of path generated
        :return: path, path distance, path elevation change
        """
        try:
            path = self.modified_dijkstra(start, end, max_length, False)
        except Exception as e:
            print(e)
            path = ssd(self.g, start, end, weight='length')[1]
        return path, self.get_path_length(path), self.get_path_length(path, elevation=True)


class MaxRouter(Router):
    """
    A Router template for maximizing path elevation
    """
    def __init__(self, g, dfs=False):
        """
        initializes a MaxRouter
        :param g: networkx graph
        :param dfs: whether to use dfs method for routing
        """
        super().__init__(g)
        self.use_dfs = dfs

    def get_route(self, start, end, max_length):
        """
        gets route, minimizing elevation gain, constrained by the max distance given
        :param start: node number for start node
        :param end: node number for end node
        :param max_length: maximum length of path generated
        :return: path, path distance, path elevation change
        """
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
    
    def simple_paths_cost(self, start, end, max_length, max_bool):
        """
        a dfs-based approach to finding all paths within a certain length for maximizing elevation
        
        heavily adapated from networkx.all_simple_paths
        :param start: node number for start node
        :param end: node number for end node
        :param max_length: maximum length of path generated
        :param max_bool: whether or not to maximize elevation
        """
        G = self.g
        seen = {}
        seen[start] = None
        generator_stack = [(vertex for connection, vertex in G.edges(start))]
        while len(stack) > 0:
            #popping from stack
            children = stack[-1]
            node = next(children, None)
            if node is None:
                seen.popitem()
                generator_stack.pop()
            elif self.get_path_length(G, seen) <= max_length and max_bool:
                if node in seen:
                    continue
                if node == target:
                    yield list(seen).append(node)
                seen[node] = None
                if target not in set(seen.keys()):
                    generator_stack.append((vertex for connection, vertex in G.edges(node)))
                else:
                    seen.popitem()
            else:
                seen.popitem()
                generator_stack.pop()
                