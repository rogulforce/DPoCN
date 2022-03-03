from pprint import pprint

import pandas as pd

from list_2.models import Edge
from models import Vertex
from models import Graph
import random
import itertools

if __name__ == "__main__":
    # # initialize vertices
    # vertex_0 = Vertex(id=0)
    # vertex_null = Vertex(id=-1)
    # vertices = [Vertex(id=1), Vertex(id=2), Vertex(id=3), Vertex(id=4), Vertex(id=5)]
    #
    # # initialize graph
    # graph = Graph()
    #
    # # add vertex to graph
    # graph.add_vertex(vertex_0)
    # graph.add_vertices_from_list(vertices)
    #
    # # check __contains__ method
    # print(vertex_0 in graph)
    # print(vertex_null in graph)
    #
    # pprint(f"vertices: {graph.get_vertices()}")
    #
    # # initialize edges
    # subsets = list(itertools.combinations(vertices, 2))
    # random.shuffle(subsets)
    # edges = []
    # for i in range(10):
    #     from_vert, to_vert = subsets[i]
    #     edge = Edge(from_vert=from_vert, to_vert=to_vert, weight=random.randint(1, 10))
    #     edges.append(edge)
    #
    # # append edges
    # graph.add_edges_from_list(edges)
    #
    # pprint(f"edges {graph.get_edges()}")
    # graph.save_graph(path="data/test_graph.txt", graph_name="test")

    graph = Graph()

    df = pd.read_csv("../list_1/data/network.csv")

    names = set(df['Unnamed: 0']) | set(df['Unnamed: 1'])

    # create vertex instances
    to_vertex = lambda x: Vertex(id=x)
    df = df.apply({"Unnamed: 0": to_vertex, "Unnamed: 1": to_vertex})

    # add verices
    graph.add_vertices_from_list([to_vertex(name) for name in names])

    # add edges
    for row in df.values:
        graph.add_edge(from_vert=row[0], to_vert=row[1])

    vert = [it for it in graph.get_vertices() if it.id == 'Alice'][0]
    print(graph.get_shortest_paths(vert))
