import networkx as nx
import numpy as np
import random
from list_3.models.utils import random_triangular


def random_graph(n: int, p: float) -> nx.Graph:
    """ function generating random not directed nx.Graph with <n> nodes and with <p> probability for connection
        between each 2 nodes.
    Args:
        n (int): number of nodes in the graph
        p (float): 0 < p < 1; probability for connection between each 2 nodes.
    Returns:
        (nx.Graph): random graph
    """
    graph = nx.Graph()

    """ add nodes """
    graph.add_nodes_from(range(n))

    """ add connections """
    rnd_tria = random_triangular(n)
    connection_cords = np.nonzero(rnd_tria > 1-p)
    graph.add_edges_from(zip(*connection_cords))
    return graph


def watts_strogatz(n: int, k: int, beta: float) -> nx.Graph:
    """ function generating nx.Graph basing on watts-strogatz model
    (https://en.wikipedia.org/wiki/Watts%E2%80%93Strogatz_model).
    Conditions: 0 <= beta <= 1, N >= k >= log(n) >= 1
    Args:
        n (int): number of nodes
        k (int): k % 2 == 0; mean degree
        beta (float): special parameter
    Returns:
        (nx.Graph): watts-strogatz model graph
    """
    if k % 2:
        raise "k must be odd number!"
    elif k > n:
        raise " k <= n"

    """ generate initial edges"""
    initial_adj_matrix = np.zeros(shape=(n, n))
    for node, row in enumerate(initial_adj_matrix):
        for to_node in range(node+1, node + k//2 + 1):
            initial_adj_matrix[node, to_node % n] = np.random.rand()
    initial_adj_matrix += initial_adj_matrix.transpose()

    """ define not yet connected nodes """
    upper_triangle = (np.triu(np.ones(shape=(n, n))) == 1)  # to work only on (j > i) indexes
    not_connected = (initial_adj_matrix == 0) & upper_triangle
    np.fill_diagonal(not_connected, 0)
    not_connected_cords = list(zip(*np.nonzero(not_connected)))

    adj_matrix = np.zeros(shape=(n,n))
    #
    # """ generate initial edges"""
    # initial_adj_matrix = np.zeros(shape=(n, n))
    # for node, row in enumerate(initial_adj_matrix):
    #     for to_node in range(node+1, node + k//2 + 1 ):
    #         initial_adj_matrix[node, to_node % n] = np.random.rand()
    # initial_adj_matrix += initial_adj_matrix.transpose()
    #
    # """ unplug initial connections by probability"""
    # adj_matrix = initial_adj_matrix > 1 - beta
    # adj_matrix = adj_matrix
    # print(adj_matrix)
    # num_of_edges_to_replace = k - (adj_matrix == 1).sum(axis=1)
    #
    # """ define not yet connected nodes """
    # not_connected = (initial_adj_matrix == 0) & upper_triangle
    # np.fill_diagonal(not_connected, 0)
    # not_connected_cords = list(zip(*np.nonzero(not_connected)))
    # print(not_connected_cords)
    #
    # """ add new connections to the remaining after unplug"""
    for node, row in enumerate(initial_adj_matrix):
        """ randomize nodes to add """
        not_connected_cords_subset = [it for it in not_connected_cords if it[0] == node]
        random.shuffle(not_connected_cords_subset)
        """ add connections """
        for i, value in enumerate(row):
            if 1 - value < beta:
                if len(not_connected_cords_subset):
                    initial_adj_matrix[node, i] = 0
                    initial_adj_matrix[i, node] = 0
                    adj_matrix[node, not_connected_cords_subset.pop()[1]] = 1

    adj_matrix += initial_adj_matrix > 0
    print(adj_matrix)
    """ generate graph, add nodes and edges """
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    connection_cords = np.nonzero(adj_matrix > 0)
    graph.add_edges_from(zip(*connection_cords))
    return graph


def barabasi_albert():
    pass


if __name__ == "__main__":
    k = watts_strogatz(13, 6, 1)
    p = nx.watts_strogatz_graph(10, 6, 1)
    print(p)
    print(k)