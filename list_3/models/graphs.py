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
        beta (float): probability of rewiring for each initial connection
    Returns:
        (nx.Graph): watts-strogatz model graph
    """
    if k % 2:
        raise nx.NetworkXError("k % 2 != 0")
    elif k > n:
        raise nx.NetworkXError(" k > n")

    nodes = list(range(n))
    graph = nx.Graph()
    graph.add_nodes_from(range(n))

    """ generate initial edges """
    for node in nodes:
        for target in range(k//2):
            graph.add_edge(node, (node + target + 1) % n)

    """ reconnect nodes according to probability """
    for node in nodes:
        # initial connections
        for target in graph[node].copy():
            if target > node:
                if np.random.rand() < beta:
                    graph.remove_edge(node, target)
                    new_connection = random.randrange(n)
                    # no self-loops, no multiple edges
                    while new_connection == node or new_connection in graph[node]:
                        new_connection = random.randrange(n)
                    graph.add_edge(node, new_connection)

    return graph


def barabasi_albert(n: int, m: int):
    """ function generating nx.Graph basing on barabasi-albert model
        (https://en.wikipedia.org/wiki/Barab%C3%A1si%E2%80%93Albert_model).
    Args:
        n (int): number of nodes
        m (int): number of connections for each node
    Returns:
        (nx.Graph): barabasi-albert model graph
    """
    nodes = list(range(n))
    graph = nx.Graph()
    graph.add_nodes_from(range(n))

    adjacency_matrix = np.zeros((n, n))

    """ initial connections """
    # connecting <m> nodes to the first node.
    adjacency_matrix[0, 1:m+1] = 1
    adjacency_matrix[1:m+1, 0] = 1

    """ add connections for new nodes"""
    # number of existing connections at this point
    sum_of_existing_edges = m
    for node in range(m+1, n):
        # define probability 
        probability = np.sum(adjacency_matrix, axis=0) / (sum_of_existing_edges * 2)

        # choose connections
        new_connections = np.random.choice(nodes, size=m, p=probability, replace=False)

        # add new connections
        adjacency_matrix[new_connections, [node] * m] = 1
        adjacency_matrix[[node] * m, new_connections] = 1

        # update existing edges counter
        sum_of_existing_edges += m

    """ add connections """
    # upper triangle to avoid adding same connection twice
    connection_cords = np.nonzero(np.triu(adjacency_matrix))
    graph.add_edges_from(zip(*connection_cords))

    return graph
