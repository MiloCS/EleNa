"""
A module that contains a number of utility functions for gathering map and elevation data
Gathers map data from osmnx and elevation data from the open elevation api
"""

import requests, networkx, pickle, os
import osmnx
from collections import OrderedDict

def input_elevations(g):
    """
    adds elevations to a osmnx networkx graph using open elevation api
    :param g: networkx graph generated by osmnx.graph.graph_from_place
    :return: new graph with elevations added
    """
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
    """
    loads the networkx biking street map of a place using osmnx
    :param place_name: string place name - town, city or other municipality type
    :return: networkx graph of place
    """
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
    """
    gets the graph of a place
    :param begin: tuple of lat, lng for start node
    :param end: tuple of lat lng for end node
    :param place: string place name - town, city or other municipality type
    :return: networkx graph of place
    """
    dist = osmnx.distance.euclidean_dist_vec(begin[1], begin[0], end[1], end[0])
    #if distance is over 10 miles apart, return False - unable to compute
    if dist > 16000:
        return False
    
    g = load_graph(place)
    return g


if __name__ == '__main__':
    mg = pickle.load(open("cache/Amherst.obj", "rb"))
