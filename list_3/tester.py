import random

import networkx as nx
import numpy as np
from models import random_triangular, random_graph


x = random_graph(5, 10)

nx.draw_networkx(x)
