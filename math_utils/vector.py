import numpy as np
from numpy import NaN, linalg

def gradient(derivatives, x):
    '''

    :param derivatives: list of MulitNumvberFunctions
    :param x: numpy array of arguments (floats)
    :return:
    '''
    assert len(derivatives) == len(x)
    gradient = np.array([derivative.evaluate(x) for derivative in derivatives])
    print(f'gradient is {gradient}')
    return gradient

def dot_product(a, b):
    '''

    :param a: numpy vector
    :param b: numpy vector
    :return: dot product of the vectors
    '''
    return np.dot(a, b)

def vector_length(vector):
    '''
    Calculates the length of the vector in euclidean space
    :param self:
    :param vector:
    :return:
    '''
    return linalg.norm(vector)