"""
index module for EleNa server
Includes routing code and a basic PathFinder class which can use different routing strategies
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json, osmnx
from gather_data import get_graph
from networkx import single_source_dijkstra as ssd
from routing import MinRouter, MaxRouter


app = Flask(__name__)
CORS(app)

@app.route('/route', methods=['POST'])
def routing():
    """
    main router function for the EleNa server
    accepts POST requests with the parameters for the search in the JSON body
    :return: jsonified path, distance and elevation change
    """
    #parameters should be called start, end, place, percent, and type
    try:
        data = request.json
        start = data['start']
        end = data['end']
        place = data['place']
        percent = data['percent']
        route_type = data['type']
    except Exception as e:
        print(e)
        return "Not all necessary parameters were included", 400

    #checking routing preconditions

    if route_type != "max" and route_type != "min":
        #bad request
        return "Type must be 'max' or 'min'", 400

    if len(start) < 2 or len(end) < 2:
        return "Start and end must each be length 2", 400

    if percent < 100 or percent > 200:
        return "Percent must be between 100 and 200", 400

    finder = PathFinder(start, end, place, percent, route_type)
    result = finder.get_path()
    return jsonify(result)

class PathFinder:
    """
    class that sets up a path search and encapsulates some utility functionality
    """
    def __init__(self, start, end, place, percent, route_type):
        """
        initializes PathFinder object with information from request
        :param start: tuple of lat, lng for start node
        :param end: tuple of lat, lng for end node
        :param place: place name string
        :param percent: int, percent of shortest path route can be
        :param route_type: string, either 'min' or 'max'
        """
        start = (float(start[0]), float(start[1]))
        end = (float(end[0]), float(end[1]))

        self.graph = get_graph(start, end, place)
        if route_type == 'min':
            self.router = MinRouter(self.graph)
        else:
            self.router = MaxRouter(self.graph)

        self.startnode = osmnx.nearest_nodes(self.graph, X=start[1], Y=start[0])
        self.endnode = osmnx.nearest_nodes(self.graph, X=end[1], Y=end[0])
        self.percent_decimal = percent / 100.0
    
    def get_path(self):
        """
        gets a path using the routing strategy determined during initialization
        :return: path list of node nums, dist of path, elevation change of path
        """
        dist, _ = ssd(self.graph, self.startnode, self.endnode, weight='length')
        route_nodes, routedist, routeele = self.router.get_route(self.startnode, self.endnode, dist * self.percent_decimal)
        #print(self.simplify_route(route_nodes))
        return self.nodes_to_info(route_nodes), routedist, routeele

    def nodes_to_info(self, path):
        """
        a helper function which creates the info needed for plotting from a list of node numbers
        :param path: list of node nums
        """
        gnodes = self.graph.nodes()
        dists = [0.0]
        for i in range(len(path) - 1):
            dists.append(self.graph[path[i]][path[i+1]][0]['length'])
        result = list(map(lambda x: gnodes[x], path))
        for i in range(len(result)):
            result[i]['dist_from_start'] = sum(dists[0:i+1])
        return result

    def simplify_route(self, path):
        """
        a helper function to simplify a route based on whether the route continues on the same street
        :param path: list of node numbers in the graph
        :return: new, simplified path node num list
        """
        new_path = []
        new_path.append(path[0])
        for i in range(1, len(path) - 1):
            try:
                e1_street = self.graph[path[i-1]][path[i]][0]['name']
                e2_street = self.graph[path[i]][path[i+1]][0]['name']
                if e1_street is not e2_street:
                    new_path.append(path[i])
            except:
                new_path.append(path[i])
        new_path.append(path[-1])
        return new_path
        


if __name__ == "__main__":
    app.run(port=8080)