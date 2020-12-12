#!/usr/bin/env python3

__author__ = "Ashot Vantsyan"
__copyright__ = "Copyright (c) 2020, Diploma project"
__version__ = "0.1"
__maintainer__ = "Ashot Vantsyan"
__email__ = "ashotvantsyan@gmail.com"
__status__ = "Dev"

import numpy as np
from itertools import permutations

def get_distance_matrix():
    matrix = np.loadtxt("city_distances.csv", delimiter=",")
    return matrix

def get_all_possible_roads(matrix):
    return permutations(range(matrix.shape[0]))

def get_distance(matrix, city1, city2):
    return matrix[city1, city2]

def get_minimal_voyage(matrix, roads, debug=False):
    best_road = None
    minimal_distance = None
    for road in roads:
        distance = 0
        for i in range(len(road)):
            distance += get_distance(matrix, road[i - 1], road[i])
        if debug:
            print(f"Road: {(road[-1],) + road}. Distance: {distance}")
        if minimal_distance is None or minimal_distance > distance:
            minimal_distance = distance
            best_road = road
    return best_road, minimal_distance


def main() -> None:
    matrix = get_distance_matrix()
    roads = get_all_possible_roads(matrix)
    road, distance = get_minimal_voyage(matrix, roads, debug=True)
    print(road, distance)

if __name__ == "__main__":
    main()