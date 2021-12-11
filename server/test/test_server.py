import sys, os
  
# setting path
sys.path.append('../')

import gather_data, routing, index
import networkx, json, flask, pickle
import pytest
from networkx import single_source_dijkstra as ssd

os.chdir('../')

@pytest.fixture
def app():
    return index.app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def graph():
    return gather_data.load_graph("Lexington, MA")

@pytest.fixture
def router(graph):
    return routing.MinRouter(graph)

@pytest.fixture
def maxrouter(graph):
    return routing.MaxRouter(graph)

# #for mocking server requests
@pytest.fixture
def construct_request():
    r = {}
    r['start'] = [42.369930, -72.508210]
    r['end'] = [42.369930, -72.508210]
    r['place'] = "Amherst, MA"
    r['percent'] = 135
    r['type'] = 'min'
    return r

#server-based testing
def test_valid_simple(client, construct_request):
    assert client.post(flask.url_for('routing'), json=construct_request).status_code == 200
    
def test_invalid_missing1(client, construct_request):
    assert client.post(flask.url_for('routing'), json=construct_request.pop('type')).status_code == 400

def test_invalid_type(client, construct_request):
    req = construct_request
    req['type'] = 'minn'
    assert client.post(flask.url_for('routing'), json=req).status_code == 400

def test_missing_vals(client):
    assert client.post(flask.url_for('routing')).status_code == 400

def test_invalid_len(client, construct_request):
    req = construct_request
    req['start'] = [1]
    assert client.post(flask.url_for('routing'), json=req).status_code == 400

def test_invalid_percent(client, construct_request):
    req = construct_request
    req['percent'] = 86
    assert client.post(flask.url_for('routing'), json=req).status_code == 400

#caching-based testing
def test_caching(graph):
    assert os.path.exists("cache/Lexington_MA.obj")

def test_cache_has_length(graph):
    assert 'length' in list(graph.edges(data=True))[0][2]

def test_cache_has_elevation(graph):
    assert 'elevation' in list(graph.nodes(data=True))[0][1]

#routing-based testing
def test_trivial_route(router):
    p, d, e = router.get_route(64058085, 64058085, 10**7)
    assert len(p) == 1
    assert d == 0
    assert e == 0

def test_len_1_route(router):
    p, d, e = router.get_route(9296568233, 476021320, 10**7)
    assert len(p) == 2
    assert d == 237.25600000000003

def test_failed_route(router):
    with pytest.raises(networkx.NetworkXNoPath):
        p, d, e = router.get_route(9296568233, 476021320, 0)

def test_min_route(graph, router):
    dist, _ = ssd(graph, 5460971028, 8195389376, weight='length')
    p, d, e = router.get_route(5460971028, 8195389376, 1.1*dist)
    assert len(p) == 61

def test_max_route(graph, maxrouter):
    dist, _ = ssd(graph, 5460971028, 8195389376, weight='length')
    p, d, e = maxrouter.get_route(5460971028, 8195389376, 1.2*dist)
    assert len(p) == 61
