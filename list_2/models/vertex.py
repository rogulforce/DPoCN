from typing import Union
# from pydantic import BaseModel
from dataclasses import dataclass, field


@dataclass
class Vertex:
    id: Union[int, str]
    # neighbours: set = field(default_factory=set)

    # def update_neighbours(self, neighbours: list) -> None:
    #     self.neighbours.update(neighbours)


# k = Vertex(id=1)
# k.neighbours.update(['x', 'xx'])
# k.neighbours.update(['x', 'xx'])
#
# print(k)