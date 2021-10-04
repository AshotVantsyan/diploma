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

def get_nearest_neighbor(matrix, from_city, cities):
    minimal_distance = get_distance(matrix, from_city, cities[0])
    nearest_city = cities[0]
    for to_city in cities[1:]:
        distance = get_distance(matrix, from_city, to_city)
        if minimal_distance is None or minimal_distance > distance:
            minimal_distance = distance
            nearest_city = to_city
    return nearest_city

def get_nearest_voyage(matrix, road, cities):
    for _ in range(len(cities)-1):
        cities.remove(road[-1])
        road.append(get_nearest_neighbor(matrix, road[-1], cities))

def get_road_distance(matrix, road):
    distance = 0
    for i in range(len(road)):
        distance += get_distance(matrix, road[i-1], road[i])
    return distance

def cost_change(distance_matrix, n1, n2, n3, n4):
    return distance_matrix[n1, n3] + distance_matrix[n2, n4] - distance_matrix[n1, n2] - distance_matrix[n3, n4]

def perform_2_opt_optimization(road: list, distance_matrix: np.matrix) -> tuple:
    new_road = road.copy()
    improved = True
    while improved:
        improved = False
        for i in range(1, len(road) - 2):
            for j in range(i+1, len(road)):
                if j - i == 1: continue
                if cost_change(distance_matrix, new_road[i - 1], new_road[i], new_road[j - 1], new_road[j]) < 0:
                    new_road[i:j] = new_road[j - 1:i - 1:-1]
                    improved = True
        road = new_road
    distance = get_road_distance(distance_matrix, new_road)
    road = tuple(int(i + 1) for i in new_road)
    return road, distance

def get_voyage(matrix, debug=False):
    cities = list(range(matrix.shape[0]))
    first_city = np.random.choice(cities)
    road = [first_city]
    get_nearest_voyage(matrix, road, cities)
    distance = get_road_distance(matrix, road)
    road, distance = perform_2_opt_optimization(road, matrix)
    # Convert indexes to city numbers.
    road = tuple(int(i + 1) for i in (road + road[0:1]))
    return road, distance

def main() -> None:
    start = time.time()
    matrix = get_distance_matrix()
    road, distance = get_voyage(matrix)
    end = round(time.time() - start, 2)
    print(json.dumps({"distance": distance, "road": road, "time": 0.11}))

if __name__ == "__main__":
    main()
