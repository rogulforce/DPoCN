import numpy as np


def random_triangular(size: int) -> np.array:
    """ function returning upper triangular random matrix with zeros on diagonal
    Args:
        size (int): size of the matrix
    Returns:
        (np.array): upper triangular random matrix with zeros on diagonal
    """
    matrix = np.zeros(shape=[size, size])
    k = 1
    for row in range(size):
        matrix[row,k:] = np.random.rand(1,size-k)
        k+=1
    return matrix


