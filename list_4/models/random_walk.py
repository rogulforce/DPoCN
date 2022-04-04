from decimal import Decimal

import numpy as np
from enum import Enum
import matplotlib.pyplot as plt
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

    def move(self, direction: tuple):
        np.add(self.position, np.array(direction), out=self.position)

    def clear(self):
        self.position = None
        self.list_of_positions = []

    def update_list_of_positions(self):
        self.list_of_positions.append(tuple(self.position))

    @staticmethod
    def choose_direction():
        return np.random.choice(list(Direction)).value

    def generate(self, starting_position: tuple = (0, 0), num_of_steps: int = 1000) -> list[tuple]:
        """ method generating random walk.
        Args:
            starting_position (tuple): starting position. Defaults to (0,0)
            num_of_steps (int): number of steps of the walk
        Returns:
            list[tuple]: list of positions.
        """
        self.position = np.array(starting_position, dtype=float)
        self.update_list_of_positions()

        for _ in range(num_of_steps):
            side = self.choose_direction()
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
        plt.savefig(f'{destination}/{self.__class__.__name__}_step_0.png')

        # change color to standard
        plt.plot(initial_position[0], initial_position[1], f'{color}o')

        prev_position = initial_position
        for i, position in enumerate(self.list_of_positions[1:]):
            plt.title(f'Random Graph. Starting position: {initial_position}, step {i+1}')

            # write with new color
            plt.plot([prev_position[0], position[0]], [prev_position[1], position[1]], f'{new_step_color}-')
            plt.plot(position[0], position[1], f'{new_step_color}o')
            plt.savefig(f'{destination}/{self.__class__.__name__}_step_{i+1}.png')

            # change color to standard
            plt.plot([prev_position[0], position[0]], [prev_position[1], position[1]], f'{color}-')
            plt.plot(position[0], position[1], f'{color}o')

            prev_position = position

        if show:
            plt.show()

        return

    def save_walk_to_gif(self, filename: str | bool = None, destination: str = 'data/', step_time: int = 1,
                         color: str = 'b', new_step_color: str = 'r'):
        """

        Args:
            filename:
            destination:
            step_time:
            color:
            new_step_color:

        Returns:

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


class PearsonRandomWalk(RandomWalk):
    """ 2 dimensional Pearson random walk class with equal probability distribution for each direction.
    Args:
        angle_precision (int): precision of angle change. Defaults to 1000
    """
    def __init__(self, angle_precision: int = 1000):
        super().__init__()
        self.angles = np.linspace(0, 2 * np.pi, angle_precision)

    def choose_direction(self) -> tuple:
        chosen_angle = np.random.choice(self.angles)
        x = np.cos(chosen_angle)
        y = np.sin(chosen_angle)
        return x, y

    def get_stats(self, num_of_trajectories: int = 100, starting_position: tuple = (0, 0), num_of_steps: int = 1000)\
                  -> tuple[list[float], list[float]]:
        right_half_fraction = []
        upper_right_fraction = []

        self.clear()

        for i in range(num_of_trajectories):
            self.generate(starting_position=starting_position, num_of_steps=num_of_steps)

            a_n = self.get_right_half_fraction(self.list_of_positions)
            b_n = self.get_upper_right_fraction(self.list_of_positions)

            right_half_fraction.append(a_n)
            upper_right_fraction.append(b_n)

            self.clear()

        return right_half_fraction, upper_right_fraction

    @staticmethod
    def get_right_half_fraction(list_of_positions):
        n = len(list_of_positions) - 1
        return len([it for it in list_of_positions[1:] if it[0] > 0]) / n

    @staticmethod
    def get_upper_right_fraction(list_of_positions):
        n = len(list_of_positions) - 1
        return len([it for it in list_of_positions[1:] if (it[0] > 0) and (it[1] > 0)]) / n


if __name__ == "__main__":
    # a = RandomWalk()
    # c = a.generate(starting_position=(3, 3), num_of_steps=10)
    # print(c)
    # # a.save_walk_to_pngs()
    # a.save_walk_to_gif(destination='../data')

    pear = PearsonRandomWalk()
    # pear_c = pear.generate(starting_position=(3, 3), num_of_steps=10)
    # print(pear_)

    # pear.save_walk_to_gif(destination='../data')

