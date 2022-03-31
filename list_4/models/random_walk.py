import numpy as np
from enum import Enum
import matplotlib.pyplot as plt
import random
import glob
import imageio
from natsort import natsorted


class Direction(Enum):
    """ dictionary of directions for reading purposes """
    UP = (0, 1)
    DOWN = (0, -1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)


class RandomWalk:
    """ 2 dimensional random walk class with equal probability distribution for each direction."""

    def __init__(self):
        self.position = None
        self.list_of_positions = []

    def move(self, direction: Direction):
        self.position += np.array(direction.value)

    def update_list_of_positions(self):
        self.list_of_positions.append(tuple(self.position))

    def generate(self, starting_position: tuple = (0,0), num_of_steps: int = 2000) -> list[tuple]:
        """ method generating random walk.
        Args:
            starting_position (tuple): starting position. Defaults to (0,0)
            num_of_steps: number of steps of the walk
        Returns:
            list[tuple]: list of postions
        """
        self.position = np.array(starting_position)
        self.update_list_of_positions()

        for _ in range(num_of_steps):
            side = np.random.choice(list(Direction))
            self.move(side)
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
        x_axis = [pos[0] for pos in self.list_of_positions]
        y_axis = [pos[1] for pos in self.list_of_positions]

        plt.figure()
        plt.grid()
        plt.xlim([min(x_axis) - 1, max(x_axis) + 1])
        plt.ylim([min(y_axis) - 1, max(y_axis) + 1])

        # initial value for first step
        initial_position = self.list_of_positions[0]
        plt.title(f'Random Graph. Starting position: {initial_position}, step 0.')

        # write with new color
        plt.plot(initial_position[0], initial_position[1], f'{new_step_color}o')
        plt.savefig(f'../{destination}/step_0.png')

        # change color to standard
        plt.plot(initial_position[0], initial_position[1], f'{color}o')

        prev_position = initial_position
        for i, position in enumerate(self.list_of_positions[1:]):
            plt.title(f'Random Graph. Starting position: {initial_position}, step {i+1}')

            # write with new color
            plt.plot([prev_position[0], position[0]], [prev_position[1], position[1]], f'{new_step_color}-')
            plt.plot(position[0], position[1], f'{new_step_color}o')
            plt.savefig(f'../{destination}/step_{i+1}.png')

            # change color to standard
            plt.plot([prev_position[0], position[0]], [prev_position[1], position[1]], f'{color}-')
            plt.plot(position[0], position[1], f'{color}o')

            prev_position = position

        if show:
            plt.show()

    def save_walk_to_gif(self, filename: str = 'random_graph.gif', destination: str = 'data/', color: str = 'b',
                         new_step_color: str = 'r'):

        self.save_walk_to_pngs(destination=destination, color=color, new_step_color=new_step_color, show=False)

        files = natsorted(glob.glob(f'../{destination}/step_*.png'))
        images = []

        for file in files:
            images.append(imageio.imread(file))
            imageio.mimsave(f'../{destination}/{filename}', images, duration=1)


if __name__ == "__main__":
    a = RandomWalk()
    c = a.generate(starting_position=(3, 3), num_of_steps=10)
    print(c)
    # a.save_walk_to_pngs()
    a.save_walk_to_gif()
