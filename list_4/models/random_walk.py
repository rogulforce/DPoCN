import numpy as np
from enum import Enum
import matplotlib.pyplot as plt
import random


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

    def save_walk(self):
        pass

    def save_walk_to_pngs(self):
        pass

    def save_walk_to_gif(self):
        self.save_walk_to_pngs()
        # TODO: add rest
        pass


if __name__ == "__main__":
    a = RandomWalk()
    c = a.generate(starting_position=(3, 3), num_of_steps=10)
    print(c)
