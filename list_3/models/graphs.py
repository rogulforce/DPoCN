import networkx as nx
import numpy as np

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
    connections = list(zip(*connection_cords))
    graph.add_edges_from(connections)
    return graph


def watts_strogatz():
    pass


def barabasi_albert():
    pass
