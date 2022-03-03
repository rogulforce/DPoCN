from list_2.models import Vertex, Edge


class Graph:
    """ Graph class.
    Attributes:
        vertices (set[Vertex]): set of graph nodes
        vertices (set[Edge]): set of graph edges
    """
    def __init__(self):
        self.vertices: list = []
        self.edges: list = []

    def add_vertex(self, vertex: Vertex) -> None:
        """ method adding to the graph 1 Vertex instance
        Args:
            vertex (Vertex): vertex to be added
        Returns:
            None
        """
        self.vertices.append(vertex)

    def add_vertices_from_list(self, vert_list: list[Vertex]):
        """ method adding to the graph list of Vertex instances
        Args:
            vert_list (list[Vertex]): vertices list to be added
        Returns:
            None
        """
        self.vertices.extend(vert_list)

    def add_edge(self, from_vert: Vertex, to_vert: Vertex, weight: int = 1):
        """ method adding to the graph Edge instance
        Args:
            from_vert (Vertex): beginning of the edge
            to_vert (Vertex): end of the edge
            weight (int): Optional. weight of the edge. Defaults to 1
        Returns:
            None
        """
        edge = Edge(from_vert=from_vert, to_vert=to_vert, weight=weight)
        self.edges.append(edge)

    def add_edges_from_list(self, edge_list: list[Edge]):
        """ method adding to the graph list of Edge instances
        Args:
            edge_list (list[Edge]): edges list to be added
        Returns:
            None
        """
        self.edges.extend(edge_list)

    def get_vertices(self) -> list:
        """ method returning all the vertices in the graph
        Returns:
            (list): list of all the vertices in the graph
        """
        return self.vertices

    def get_edges(self) -> list:
        """ method returning all the edges in the graph
        Returns:
            (list): list of all the edges in the graph
        """
        return self.edges

    def get_neighbours(self, vert_key: Vertex) -> list:
        """ method returning all the neighbours of the given vertex
        Args:
            vert_key (Vertex): investigated vertex
        Returns:
            (list): list of all neighbours of vert_key
        """

        neighbours = []
        for edge in self.edges:
            if edge.from_vert == vert_key:
                neighbours.append(edge.to_vert)
            elif edge.to_vert == vert_key:
                neighbours.append(edge.from_vert)
        return neighbours

    def __contains__(self, vertex: Vertex) -> bool:
        """ method checking if the given Vertex is in the graph.
        Args:
            vertex (Vertex): investigated vertex.
        Returns:
            (bool): True for a statement of the form vertex in graph, if the given vertex is in the graph,
                    False otherwise.
        """
        return vertex in self.vertices

    def save_graph(self, path: str, graph_name: str = ""):
        """ method saving the graph in dot format to the given file.
        Args:
            path (str): path of the file for the graph to be saved
            graph_name (str): Optional. name of the graph. Defaults to ""
        Returns:
            None
        """
        with open(path, "w+") as file:
            file.write(f"graph {graph_name} {{\n")
            for edge in self.get_edges():
                line = f"{edge.from_vert.id} -- {edge.to_vert.id} [weight={edge.weight}]"
                file.write(line + "\n")
            file.write("}")

    def get_shortest_paths(self, from_vert) -> dict:
        """ function returning the shortest path from given vert to all other verts. My own idea and implementation.
        1. start with the from_vert node. path_len = 1. Define neghbours
        2. for each neighbour set actual path_len, then:
        path_len += 1
        repeat for each of the list of 'not visited' neighbours of the neighbours until we cover all neighbours.

        Args:
            from_vert: starting vert
        Returns:
            (dict): Neighbour: shortest_path_length
        """
        shortest_path = {}
        path_len = 1

        not_visited_nodes = self.vertices
        not_visited_nodes.remove(from_vert)  # remove initial node

        # list of neighbours with their path len to the initial node
        neighbours = self.get_neighbours(from_vert)
        neighbours_wt_path = [(node, path_len) for node in neighbours]

        # set neighbours as visited (queued to be visited)
        not_visited_nodes = [node for node in not_visited_nodes if node not in neighbours]

        while neighbours_wt_path:  # while the list is not empty
            # take 'the oldest' neighbour with his path length
            node, path_len = neighbours_wt_path.pop(0)

            # set his path length
            shortest_path[node.id] = path_len

            # define new neighbours with path_len += 1
            new_neighbours = [new_node for new_node in self.get_neighbours(node)
                              if new_node in not_visited_nodes]
            n_n_wt_path = [(new_node, path_len+1) for new_node in new_neighbours]

            # set new neighbours as already visited (queued to be visited)
            not_visited_nodes = [node for node in not_visited_nodes if node not in new_neighbours]

            # add them to the queue
            neighbours_wt_path.extend(n_n_wt_path)
        return shortest_path



