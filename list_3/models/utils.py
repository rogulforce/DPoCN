import networkx as nx
import numpy as np
from pydantic import BaseModel


def random_triangular(size: int) -> np.array:
    """ function returning upper triangular random matrix with zeros on diagonal
    Args:
        size (int): size of the matrix
    Returns:
        (np.array): upper triangular random matrix with zeros on diagonal
    """
    matrix = np.zeros(shape=[size, size])
    k = 1
    for row in range(size):
        matrix[row,k:] = np.random.rand(1,size-k)
        k+=1
    return matrix


class Stat(BaseModel):
    vertices: int
    edges: int
    mean_degree: float
    var_degree: float


def show_statistics(graph: nx.Graph) -> dict:
    """ function returning dict of base statistics of given <graph>.
    Args:
        graph (nx.Graph): graph instance
    Returns:
        (dict): dict containing base statistics of given graph
    """
    degree = [it[1] for it in graph.degree]
    stat = Stat(vertices=graph.number_of_nodes(), edges=graph.number_of_edges(), mean_degree=np.mean(degree),
                var_degree=np.var(degree))
    return stat.dict()


