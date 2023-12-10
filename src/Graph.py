import networkx as nx
import random


def get_random_simple_Gnp_graph(n, seed=42):
    '''
    The function generates an undirected unweighted graph as an adjacency list
    '''
    edge_p = 1/2  # probability of an edge between vertices 0.5
    g = nx.random_graphs.fast_gnp_random_graph(n, edge_p, seed)
    return nx.convert.to_dict_of_lists(g)


def generate_graph(number_of_vertex, max_weight=10, min_weight=1):
    '''
    Generation of a weighted undirected graph with edge weights from 1 to 10
    '''
    graph_without_weights = get_random_simple_Gnp_graph(number_of_vertex)
    weighted_graph = {}

    for node in graph_without_weights:
        weighted_graph[node] = {}
        for neighbor in graph_without_weights[node]:
            # Assigning a random weight to an edge
            weighted_graph[node][neighbor] = random.randint(
                min_weight, max_weight)
            # Adding a back edge to an undirected graph
            if neighbor not in weighted_graph:
                weighted_graph[neighbor] = {}
            weighted_graph[neighbor][node] = weighted_graph[node][neighbor]

    res_graph = []
    for vert in weighted_graph:
        res_graph.append(list(weighted_graph[vert].items()))

    return res_graph
