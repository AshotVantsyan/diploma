#!/usr/bin/env python3

__author__ = "Ashot Vantsyan"
__copyright__ = "Copyright (c) 2020, Diploma project"
__version__ = "0.1"
__maintainer__ = "Ashot Vantsyan"
__email__ = "ashotvantsyan@gmail.com"
__status__ = "Dev"


import numpy as np

def get_distance_matrix():
    matrix = np.loadtxt("city_distances.csv", delimiter=",")
    return matrix

def get_distance(matrix, city1, city2):
    return matrix[city1, city2]

def get_random_voyage(matrix, debug=False):
    road = tuple(np.random.permutation(range(matrix.shape[0])))
    distance = 0
    for i in range(len(road)):
        distance += get_distance(matrix, road[i - 1], road[i])
    if debug:
        print(f"Road: {(road[-1],) + road}. Distance: {distance}")
    return road, distance


def main() -> None:
    matrix = get_distance_matrix()
    road, distance = get_random_voyage(matrix, debug=False)
    print(road, distance)

if __name__ == "__main__":
    main()