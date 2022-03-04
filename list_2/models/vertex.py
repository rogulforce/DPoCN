from typing import Union
from dataclasses import dataclass, field


@dataclass
class Vertex:
    """ Vertex class
    Attributes:
        id (Union[int,str]): id of the node
    """
    id: Union[int, str]
