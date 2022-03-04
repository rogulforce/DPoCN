from dataclasses import dataclass
from list_2.models import Vertex


@dataclass
class Edge:
    """ Vertex class
    Attributes:
        from_vert (Vertex): beginning of the edge
        from_vert (Vertex): end of the edge
        weight (int): Weight of the edge. Defaults to 1
    """
    from_vert: Vertex
    to_vert: Vertex
    weight: int = 1
