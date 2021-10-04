#!/usr/bin/env python3

__author__ = "Ashot Vantsyan"
__copyright__ = "Copyright (c) 2020, Diploma project"
__version__ = "1.0"
__maintainer__ = "Ashot Vantsyan"
__email__ = "ashotvantsyan@gmail.com"
__status__ = "Released"

import os
import json
import time
import numpy as np

def get_distance_matrix():
    file = os.getenv("DISTANCE_FILE", "city_distances.csv")
    matrix = np.loadtxt(file, delimiter=",")
    return np.matrix(matrix)

def get_distance(matrix, city1, city2):
    return matrix[city1, city2]

def generate_road(matrix):
    yield 0
    for i in np.random.permutation(range(1, matrix.shape[0])):
        yield int(i)
    yield 0

def get_road_distance(matrix, road):
    distance = 0
    for i in range(1, len(road)):
        distance += get_distance(matrix, road[i-1], road[i])
    return distance

def get_voyage(matrix, debug=False):
    road = list(generate_road(matrix))
    number_of_cities = len(road)
    distance = get_road_distance(matrix, road)
    temperature = start_temperature = 10000
    for k in range(1, 10000):
        potential_road = road.copy()
        i, j = sorted(np.random.choice(range(number_of_cities)[1:-1], 2, replace=False))
        potential_road[i], potential_road[j] = potential_road[j], potential_road[i]
        potential_distance = get_road_distance(matrix, potential_road)
        if potential_distance < distance:
            road = potential_road
            distance = potential_distance
        else:
            probability = np.exp((-(potential_distance - distance)) / temperature)
            if np.random.random_sample() <= probability:
                road = potential_road
                distance = potential_distance
        temperature = start_temperature / (k/2)
        if temperature < 1:
            break
        if debug:
            print(f"Temperature: {temperature}, Distance: {distance}")
    road = tuple(int(i + 1) for i in road)
    return road, distance

def main() -> None:
    matrix = get_distance_matrix()
    start = time.time()
    road, distance = get_voyage(matrix)
    end = round(time.time() - start, 2)
    print(json.dumps({"distance": distance, "road": road, "time": end}))

if __name__ == "__main__":
    main()
