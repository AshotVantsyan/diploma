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

def get_voyage(matrix, debug=False):
    cities = list(range(matrix.shape[0]))
    first_city = np.random.choice(cities)
    road = [first_city]
    get_nearest_voyage(matrix, road, cities)
    distance = get_road_distance(matrix, road)
    # Convert indexes to city numbers.
    road = tuple(int(i + 1) for i in (road + road[0:1]))
    return road, distance

def main() -> None:
    matrix = get_distance_matrix()
    road, distance = get_voyage(matrix)
    print(json.dumps({"distance": distance, "road": road}))

if __name__ == "__main__":
    main()