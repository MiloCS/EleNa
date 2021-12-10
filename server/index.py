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

    if route_type != "max" and route_type != "min":
        #bad request
        return "Type must be 'max' or 'min'", 400
    finder = PathFinder(start, end, place, percent, route_type)
    result = finder.get_path()
    return jsonify(result)

class PathFinder:
    def __init__(self, start, end, place, percent, route_type):
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
        dist, _ = ssd(self.graph, self.startnode, self.endnode, weight='length')
        route_nodes, routedist, routeele = self.router.get_route(self.startnode, self.endnode, dist * self.percent_decimal)
        gnodes = self.graph.nodes()
        result = list(map(lambda x: gnodes[x], self.simplify_route(route_nodes)))
        #print(self.simplify_route(route_nodes))
        return result, routedist, routeele

    def simplify_route(self, path):
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