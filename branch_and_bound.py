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

def get_minimal_voyage(matrix, roads, debug=False):
    best_road = None
    minimal_distance = None
    return best_road, minimal_distance


def main() -> None:
    matrix = get_distance_matrix()
    roads = None
    road, distance = get_minimal_voyage(matrix, roads, debug=False)
    print(road, distance)

if __name__ == "__main__":
    main()