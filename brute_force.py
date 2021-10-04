#!/usr/bin/env python3

__author__ = "Ashot Vantsyan"
__copyright__ = "Copyright (c) 2020-2021, Diploma project"
__email__ = "ashotvantsyan@gmail.com"
__maintainer__ = "Ashot Vantsyan"
__status__ = "Released"
__version__ = "1.1"

import os
import json
import time
import numpy as np
from typing import Iterable, Union
from itertools import permutations

def get_distance_matrix() -> np.matrix:
    file = os.getenv("DISTANCE_FILE", "city_distances.csv")
    matrix = np.loadtxt(file, delimiter=",")
    return np.matrix(matrix)

def get_all_possible_roads(matrix: np.matrix) -> Iterable:
    return permutations(range(matrix.shape[0]))

def get_distance(matrix: np.matrix, city1: int, city2: int):
    return matrix[city1, city2]

def get_minimal_voyage(matrix: np.matrix, roads: Iterable, debug: bool = False) -> tuple:
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
    # Convert indexes to city numbers.
    best_road = tuple(i + 1 for i in (best_road + best_road[0:1]))
    return best_road, minimal_distance

def main() -> None:
    start = time.time()
    matrix = get_distance_matrix()
    roads = get_all_possible_roads(matrix)
    road, distance = get_minimal_voyage(matrix, roads)
    end = round(time.time() - start, 2)
    print(json.dumps({"distance": distance, "road": road, "time": end}))

if __name__ == "__main__":
    main()
