from list_2.models import Vertex, Edge
import numpy as np


class Graph:
    """ Graph class.
    Attributes:
        vertices (set[Vertex]): set of graph nodes
        edges (set[Edge]): set of graph edges
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

    def get_weighted_neighbours(self, vert_key: Vertex) -> list[tuple]:
        """ method returning all the neighbours of the given vertex
        Args:
            vert_key (Vertex): investigated vertex
        Returns:
            (list[tuple]): list of tuples of all neighbours of vert_key with weight of the connection
        """

        weighted_neighbours = []
        for edge in self.edges:
            if edge.from_vert == vert_key:
                weighted_neighbours.append((edge.to_vert, edge.weight))
            elif edge.to_vert == vert_key:
                weighted_neighbours.append((edge.from_vert, edge.weight))
            return weighted_neighbours

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
        """ function returning the shortest path from given vert to all other verts.
        Known in literature as 'breadth-first search'
        Args:
            from_vert: starting vert
        Returns:
            (dict): dictionary of these elements of the graph which you initial node can reach in convention
                    {node.id: shortest_path_length}
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
            # take first node from the queue
            node, path_len = neighbours_wt_path.pop(0)

            # save the path length to result list
            shortest_path[node.id] = path_len

            # define neighbours of the node (set their path_len += 1)
            new_neighbours = [new_node for new_node in self.get_neighbours(node)
                              if new_node in not_visited_nodes]
            n_n_wt_path = [(new_node, path_len+1) for new_node in new_neighbours]  # n_n -> new_neighbours

            # set new neighbours as visited (in fact they are queued to be visited)
            not_visited_nodes = [node for node in not_visited_nodes if node not in new_neighbours]

            # add new neighbours to the queue
            neighbours_wt_path.extend(n_n_wt_path)
        return shortest_path

    def get_weighted_shortest_paths(self, from_vert) -> dict:
        """ function returning the shortest path from given vert to all other verts.
        Known in literature as 'breadth-first search'
        Args:
            from_vert: starting vert
        Returns:
            (dict): dictionary of these elements of the graph which you initial node can reach in convention
                    {node.id: shortest_path_length}
        """
        # TODO: zmieni?? na wa??ony - przechodzisz dalej jedynie je??li masz kr??tsz drog??
        shortest_path = {node.id: np.inf for node in self.vertices}
        shortest_path[from_vert.id] = 0

        # list of neighbours with their path weight to the initial node
        neighbours_weighted = self.get_weighted_neighbours(from_vert)

        while neighbours_weighted:  # while the list is not empty
            # take first node from the queue
            node, path_weight = neighbours_weighted.pop(0)

            # save the path weight to result list
            shortest_path[node.id] = path_weight

            # add new neighbours with previous path weight
            new_neighbours = [(neighbour[0], neighbour[1] + path_weight) for
                              neighbour in self.get_weighted_neighbours(node)]

            # add only these neighbours with shorter path than already existing
            neighbours_to_queue = [it for it in new_neighbours if it[1] < shortest_path[it[0]]]

            # add new neighbours to the queue
            neighbours_weighted.extend(neighbours_to_queue)
        return shortest_path
