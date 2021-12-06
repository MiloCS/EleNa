import requests, osmnx, networkx, pickle, os
from collections import OrderedDict

def input_elevations(g):
    elevation_dict = {}
    outer_param_dict = {}
    inner_param_list = []
    nodes = OrderedDict(g.nodes(data=True))
    for key in nodes:
        nodeval = nodes[key]
        inner_dict = {}
        inner_dict["latitude"] = nodeval['y']
        inner_dict["longitude"] = nodeval['x']
        inner_param_list.append(inner_dict)
    outer_param_dict['locations'] = inner_param_list
    outer_param_dict = requests.post('https://api.open-elevation.com/api/v1/lookup', data=outer_param_dict)

    networkx.set_node_attributes(g, elevation_dict, name='elevation')
    return g

def load_graph(place_name):
    file_name = "_".join(place_name.replace(" ", "").split(",")) + ".obj"
    if file_name in os.walk("/cache"):
        with open("/cache/" + file_name, "rb") as f:
            g = pickle.load(f)
    else:
        g = osmnx.graph.graph_from_place(place_name, network_type='bike')
        g = input_elevations(g)
        with open("/cache/" + file_name, "rb") as f:
            pickle.dump(g, f) 
    return g


def get_graph(begin, end, place):
    dis = osmnx.distance.euclidean_dist_vec(begin[1], begin[0], end[1], end[0])
    if dist > 3200:
        return False
    
    g = load_graph(place)
    return g



