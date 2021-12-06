from flask import Flask, request, jsonify
import json, osmnx
from gather_data import get_graph
from networkx import single_source_dijkstra as ssd
from routing import MinRouter, MaxRouter

app = Flask(__name__)

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
    end = (float(start[0]), float(start[1]))

    graph = get_graph(start, end, place)
    if route_type == 'min':
        router = MinRouter(graph)
    else:
        router = MaxRouter(graph)

    startnode = osmnx.distance.get_nearest_node(graph, start)
    endnode = osmnx.distance.get_nearest_node(graph, end)
    print(startnode)
    print(endnode)
    
    percent_decimal = percent / 100.0
    dist, _ = ssd(graph, startnode, endnode, weight='length')
    return router.get_route(startnode, endnode, dist * percent_decimal)


if __name__ == "__main__":
    app.run(port=8080)