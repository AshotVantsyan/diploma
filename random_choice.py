#!/usr/bin/env python3

__author__ = "Ashot Vantsyan"
__copyright__ = "Copyright (c) 2020, Diploma project"
__version__ = "0.1"
__maintainer__ = "Ashot Vantsyan"
__email__ = "ashotvantsyan@gmail.com"
__status__ = "Dev"

import os
import json
import numpy as np

def get_distance_matrix():
    file = os.getenv("DISTANCE_FILE", "city_distances.csv")
    matrix = np.loadtxt(file, delimiter=",")
    return np.matrix(matrix)

def get_distance(matrix, city1, city2):
    return matrix[city1, city2]

def get_random_voyage(matrix, debug=False):
    road = tuple(np.random.permutation(range(matrix.shape[0])))
    distance = 0
    for i in range(len(road)):
        distance += get_distance(matrix, road[i - 1], road[i])
    if debug:
        print(f"Road: {(road[-1],) + road}. Distance: {distance}")
    # Convert indexes to city numbers.
    road = tuple(int(i + 1) for i in (road + road[0:1]))
    return road, distance


def main() -> None:
    matrix = get_distance_matrix()
    road, distance = get_random_voyage(matrix, debug=False)
    print(json.dumps({"distance": distance, "road": road}))

if __name__ == "__main__":
    main()