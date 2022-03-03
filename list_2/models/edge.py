from dataclasses import dataclass
from list_2.models import Vertex



@dataclass
class Edge:
    from_vert: Vertex
    to_vert: Vertex
    weight: int = 1
