import glob
from copy import copy

import imageio
import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
from natsort import natsorted

from list_3.models import random_graph


class RandomWalkOnGraph:
 
    def __init__(self, network: nx.Graph | bool = None):
        self._network = network
        self.position = None
        self.list_of_positions = []

    @property
    def network(self):
        return self._network

    @network.setter
    def network(self, network: nx.Graph):
        self._network = network

    def clear(self):
        self.position = None
        self.list_of_positions = []

    def choose_direction(self):
        """ function choosing direction for random walk on graph"""
        neighbors = [it for it in self._network.neighbors(self.position)]
        if neighbors:
            return np.random.choice(neighbors)
        else:
            # if there are no neighbours we just don't move.
            return self.position

    def move(self, direction):
        self.position = direction

    def update_list_of_positions(self):
        self.list_of_positions.append(self.position)

    def generate(self, starting_position: int = 0, num_of_steps: int = 1000) -> list[tuple]:
        """ method generating a walk.
        Args:
            starting_position (int): starting position. Defaults to (0,0)
            num_of_steps (int): number of steps of the walk
        Returns:
            list[tuple]: list of positions.
        """
        self.position = starting_position
        self.update_list_of_positions()

        for _ in range(num_of_steps):
            direction = self.choose_direction()
            self.move(direction)
            self.update_list_of_positions()

        return self.list_of_positions

    def save_walk_to_pngs(self, filename: str | bool = None, destination: str = 'data/', color: str = 'b', new_step_color: str = 'r',
                          prev_color='g',show: bool = False):
        """ function saving each move (with old moves before it) to png
        Args:
            filename (str | bool): custom filename.
            destination (str): folder destination. Defaults to 'data/'.
            color (str): color of the walk. Defaults to 'b'
            new_step_color (str): color of newly added step to the walk. Defaults to 'r'
            show (bool): plt.show() indicator. Defaults to False
        """
        if not filename:
            filename = f'{self.__class__.__name__}'

        layout = nx.circular_layout(self._network)

        plt.figure()
        # initial value for first step
        initial_position = self.list_of_positions[0]
        plt.title(f'Random walk on graph. Starting position: {initial_position}, step 0.')

        # write with new color
        nx.draw_networkx(self._network, pos=layout, node_color=color, edge_color=color)
        nx.draw_networkx_nodes([initial_position], pos=layout, node_color=new_step_color)
        plt.savefig(f'{destination}/{filename}_step_0.png')

        # change color to standard
        nx.draw_networkx_nodes([initial_position], pos=layout, node_color=prev_color)

        prev_position = initial_position
        for i, position in enumerate(self.list_of_positions[1:]):
            plt.title(f'Random walk on graph. Starting position: {initial_position}, step {i + 1}')

            # write with new color
            nx.draw_networkx_nodes([position], pos=layout, node_color=new_step_color)
            nx.draw_networkx_edges(self._network, edgelist=[(prev_position, position)], pos=layout,
                                   edge_color=new_step_color)
            plt.savefig(f'{destination}/{filename}_step_{i + 1}.png')

            # change color to standard
            nx.draw_networkx_nodes([position], pos=layout, node_color=prev_color)
            nx.draw_networkx_edges(self._network, edgelist=[(prev_position, position)], pos=layout,
                                   edge_color=prev_color)

            prev_position = position

        if show:
            plt.show()

    def save_walk_to_gif(self, filename: str | bool = None, destination: str = 'data/', step_time: int = 1,
                         color: str = 'b', new_step_color: str = 'r', prev_color='g') -> None:
        """ function saving the walk to a gif.
        Args:
            filename: name of the file.
            destination: name of the folder.
            step_time: waiting time for GIF to change picture.
            color: color of the plot.
            new_step_color: color of new step in trajectory.
        Returns:
            None
        """
        if not filename:
            filename = f'{self.__class__.__name__}'

        self.save_walk_to_pngs(filename=filename, destination=destination, color=color, new_step_color=new_step_color,
                               prev_color=prev_color, show=False)

        files = natsorted(glob.glob(f'{destination}/{filename}_step_*.png'))
        images = []

        for file in files:
            images.append(imageio.imread(file))
            imageio.mimsave(f'{destination}/{filename}.gif', images, duration=step_time)
        return

    def get_stats(self, starting_node: int = 0, max_iter: int = 1000):
        """
        Args:
            starting_node:
            max_iter:
        Returns:
        """

        nodes = list(self._network.nodes)

        unvisited_nodes = copy(nodes)
        unvisited_nodes.remove(starting_node)
        time_to_hit = {it: np.inf for it in unvisited_nodes}

        i = 1
        self.move(starting_node)
        while i <= max_iter and unvisited_nodes:
            current_node = self.choose_direction()
            self.move(current_node)

            if current_node in unvisited_nodes:
                unvisited_nodes.remove(current_node)
                time_to_hit[current_node] = i
            i += 1
        return time_to_hit


if __name__ == "__main__":
    x = random_graph(10, .2)
    rwog = RandomWalkOnGraph()
    rwog.network = x

    nx.draw_networkx(x, pos=nx.circular_layout(x))
    plt.show()

    mc = 100
    stats = rwog.get_stats()
    for _ in range(mc-1):
        new_stats = rwog.get_stats()
        stats = {key: val + new_stats[key] for key, val in stats.items()}

    print({key: val/mc for key, val in stats.items()})