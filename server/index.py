from flask import Flask, request, jsonify
from flask_cors import CORS
import json, osmnx
from gather_data import get_graph
from networkx import single_source_dijkstra as ssd
from networkx.readwrite import json_graph
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

    result = get_path(start, end, place, percent, route_type)
    return jsonify(result)

def get_path(start, end, place, percent, route_type):
    start = (float(start[0]), float(start[1]))
    end = (float(end[0]), float(end[1]))


    graph = get_graph(start, end, place)
    if route_type == 'min':
        router = MinRouter(graph)
    else:
        router = MaxRouter(graph)

    startnode = osmnx.nearest_nodes(graph, X=start[1], Y=start[0])
    endnode = osmnx.nearest_nodes(graph, X=end[1], Y=end[0])
    
    percent_decimal = percent / 100.0
    dist, _ = ssd(graph, startnode, endnode, weight='length')
    route_nodes = router.get_route(startnode, endnode, dist * percent_decimal)
    print(route_nodes)
    gnodes = graph.nodes()
    result = list(map(lambda x: gnodes[x], route_nodes[1]))
    return result


if __name__ == "__main__":
    app.run(port=8080)