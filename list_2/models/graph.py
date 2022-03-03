

class Graph:
    """ Graph class.
    Attributes:
        vertices (set[Vertex]): set of graph nodes
        vertices (set[Edge]): set of graph edges
    """
    def __init__(self):
        self.vertices = {}
        self.edges = {}

    def add_vertex(self):
        pass

    def add_vertices_from_list(self, vert_list: list):
        pass

    def add_edge(self, from_vert, to_vert):
        pass

    def add_weighted_edge(self, from_vert, to_vert, weight):
        pass

    def add_edges_from_list(self, edge_list: list):
        pass

    def get_vertices(self) -> list:
        pass

    def get_edges(self) -> list:
        pass

    def get_neighbours(self, vert_key) -> list:
        pass

    # def __repr__(self):
    #     return 'x'

    def save_graph(self, graph):
        pass

    def get_shortest_paths(self, from_vert):
        pass
