import glob
import imageio
import networkx
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
        return np.random.choice(neighbors)

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

    def save_walk_to_pngs(self, destination: str = 'data/', color: str = 'b', new_step_color: str = 'r',
                          show: bool = False):
        """ function saving each move (with old moves before it) to png
        Args:
            destination (str): folder destination. Defaults to 'data/'.
            color (str): color of the walk. Defaults to 'b'
            new_step_color (str): color of newly added step to the walk. Defaults to 'r'
            show (bool): plt.show() indicator. Defaults to False
        """
        layout = networkx.circular_layout(self._network)

        plt.figure()
        # initial value for first step
        initial_position = self.list_of_positions[0]
        plt.title(f'Random Graph. Starting position: {initial_position}, step 0.')

        # write with new color
        nx.draw_networkx(self._network, pos=layout, node_color=color, edge_color=color)
        nx.draw_networkx_nodes([initial_position], pos=layout, node_color=new_step_color)
        plt.savefig(f'{destination}/{self.__class__.__name__}_step_0.png')

        prev_position = initial_position
        for i, position in enumerate(self.list_of_positions[1:]):
            plt.title(f'Random Graph. Starting position: {initial_position}, step {i + 1}')

            # write with new color
            nx.draw_networkx_nodes([prev_position, position], pos=layout, node_color=new_step_color)
            nx.draw_networkx_edges(self._network, edgelist=[(prev_position, position)], pos=layout, edge_color=new_step_color)
            plt.savefig(f'{destination}/{self.__class__.__name__}_step_{i + 1}.png')

            # change color to standard
            nx.draw_networkx_nodes([prev_position, position], pos=layout, node_color=color)
            nx.draw_networkx_edges(self._network, edgelist=[(prev_position, position)], pos=layout, edge_color=color)

            prev_position = position

        if show:
            plt.show()

    def save_walk_to_gif(self, filename: str | bool = None, destination: str = 'data/', step_time: int = 1,
                         color: str = 'b', new_step_color: str = 'r') -> None:
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
            filename = f'{self.__class__.__name__}.gif'

        self.save_walk_to_pngs(destination=destination, color=color, new_step_color=new_step_color, show=False)

        files = natsorted(glob.glob(f'{destination}/{self.__class__.__name__}_step_*.png'))
        images = []

        for file in files:
            images.append(imageio.imread(file))
            imageio.mimsave(f'{destination}/{filename}', images, duration=step_time)
        return

    def get_stats(self):
        pass


if __name__ == "__main__":
    x = random_graph(10, .5)
    rwog = RandomWalkOnGraph()
    rwog.network = x

    print(rwog.generate(num_of_steps=5))
    # rwog.save_walk_to_pngs()
    rwog.save_walk_to_gif(destination='../data')
