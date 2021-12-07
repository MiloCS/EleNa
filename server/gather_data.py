import requests, networkx, pickle, os
import osmnx
from collections import OrderedDict
from routing import simple_paths_cost

def input_elevations(g):
    outer_param_dict = {}
    inner_param_list = []
    nodes = OrderedDict(g.nodes(data=True))
    max_request_length = 1000
    
    #building list of lats and lngs
    for key in nodes:
        nodeval = nodes[key]
        inner_dict = {}
        inner_dict["latitude"] = nodeval['y']
        inner_dict["longitude"] = nodeval['x']
        inner_param_list.append(inner_dict)

    ipl_len = len(inner_param_list)

    #performing a series of requests to the elevation api
    results = []
    curr_index = 0
    headers_dict = {"Content-Type": "application/json", "Accept": "application/json"}
    while curr_index < ipl_len:
        if curr_index+max_request_length < ipl_len:
            inner_param_list_sect = inner_param_list[curr_index:curr_index+max_request_length]
        else:
            inner_param_list_sect = inner_param_list[curr_index:]
        outer_param_dict["locations"] = inner_param_list_sect
        result_locations = requests.post('https://api.open-elevation.com/api/v1/lookup', json=outer_param_dict, headers=headers_dict)
        result_locations = result_locations.json()['results']
        results.extend(result_locations)
        curr_index += max_request_length
    
    #loading elevation data into format that can be added to graph
    elevation_dict = {}
    for i, key in enumerate(nodes.keys()):
        elevation_dict[key] = results[i]['elevation']
    networkx.set_node_attributes(g, elevation_dict, name='elevation')
    return g

def load_graph(place_name):
    file_name = "_".join(place_name.replace(" ", "").split(",")) + ".obj"
    if file_name in os.listdir("cache"):
        with open("cache/" + file_name, "rb") as f:
            g = pickle.load(f)
    else:
        with open("cache/" + file_name, "wb+") as f:
            g = osmnx.graph.graph_from_place(place_name, network_type='bike')
            g = input_elevations(g)
            pickle.dump(g, f) 
    return g


def get_graph(begin, end, place):
    dist = osmnx.distance.euclidean_dist_vec(begin[1], begin[0], end[1], end[0])
    if dist > 3200:
        return False
    
    g = load_graph(place)
    return g


if __name__ == '__main__':
    mg = pickle.load(open("cache/Amherst.obj", "rb"))
    print(mg[9056574307][9056578512])
    paths = simple_paths_cost(mg, 9056574307, 9056578512, 60.0)
    print(mg[9056574307][8320711505])
    print(paths)
    # l = networkx.all_simple_paths(mg, 9052567911, 9049627073, cutoff=100)
    # c = next(l)
    # print(c)
