I've decided to change:

1. naming convention to more modern with underscores, 

ex. 
* _addVertex()_ -> _add_vertex()_
* _addVerticesFromList(vertList)_ -> _add_vertices_from_list(vert_list)_

2. add_edge method takes optional parameter _weight_: int = 1 to avoid creating 2 method with the same usage.
