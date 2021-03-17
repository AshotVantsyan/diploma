#!/usr/bin/env python3

__author__ = "Ashot Vantsyan"
__copyright__ = "Copyright (c) 2020-2021, Diploma project"
__maintainer__ = "Ashot Vantsyan"
__email__ = "ashotvantsyan@gmail.com"
__version__ = "1.0"
__status__ = "Released"

import os
import sys
import json
import copy
import numpy as np

mask = {}
all_sets = []
solutions = []

def get_distance_matrix() -> np.matrix:
    file = os.getenv("DISTANCE_FILE", "city_distances.csv")
    matrix = np.loadtxt(file, delimiter=",")
    return np.matrix(matrix)

def get_minimum(matrix, tour, rest_of_cities):
    if (tour, rest_of_cities) in mask:
        return mask[tour, rest_of_cities]
    values = []
    all_min = []
    for j in rest_of_cities:
        city_set = copy.deepcopy(list(rest_of_cities))
        city_set.remove(j)
        all_min.append([j, tuple(city_set)])
        result = get_minimum(matrix, j, tuple(city_set))
        values.append(matrix[tour-1, j-1] + result)
    mask[tour, rest_of_cities] = min(values)
    solutions.append(((tour, rest_of_cities), all_min[values.index(mask[tour, rest_of_cities])]))
    return mask[tour, rest_of_cities]

def get_minimal_voyage(matrix: np.matrix) -> tuple:
    for i in range(1, matrix.shape[0]):
        mask[i + 1, ()] = matrix[i, 0]
    get_minimum(matrix, 1, range(2, matrix.shape[0] + 1))
    road = [1]
    solution = solutions.pop()
    road.append(solution[1][0])
    for _ in range(matrix.shape[0] - 2):
        for new_solution in solutions:
            if tuple(solution[1]) == new_solution[0]:
                solution = new_solution
                road.append(solution[1][0])
                break
    road.append(1)
    road = tuple(road)
    distance = mask[1, range(2, matrix.shape[0] + 1)]
    return road, distance

def main():
    matrix = get_distance_matrix()
    road, distance = get_minimal_voyage(matrix)
    print(json.dumps({"distance": distance, "road": road}))


if __name__ == '__main__':
    main()