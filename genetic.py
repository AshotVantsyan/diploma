#!/usr/bin/env python3

__author__ = "Ashot Vantsyan"
__copyright__ = "Copyright (c) 2020, Diploma project"
__version__ = "0.1"
__maintainer__ = "Ashot Vantsyan"
__email__ = "ashotvantsyan@gmail.com"
__status__ = "Dev"

import os
import time
import json
import numpy as np

def get_distance_matrix() -> np.matrix:
    file = os.getenv("DISTANCE_FILE", "city_distances.csv")
    matrix = np.loadtxt(file, delimiter=",")
    return np.matrix(matrix)

def get_road_distance(matrix, road):
    distance = 0
    for i in range(len(road)):
        distance += matrix[road[i-1], road[i]]
    return distance

class Chromosome:
    population = []
    total_distance = 0

    @classmethod
    def add_to_population(cls, chromosome):
        cls.population.append(chromosome)
        cls.total_distance += chromosome.distance

    @classmethod
    def remove_from_population(cls, start, end):
        for i in range(start, end):
            cls.total_distance -= Chromosome.population.pop(i).distance

    @classmethod
    def sort_population(cls):
        cls.population.sort(key=lambda chromosome: chromosome.distance)

    def __init__(self, road=None):
        self.road = np.array(np.random.permutation(range(matrix.shape[0]))) if road is None else road
        self.distance = get_road_distance(matrix, self.road)
        if debug:
            print(f"Road: {self.road}, Distance: {self.distance}")
        Chromosome.add_to_population(self)

def generate_initial_population():
    for _ in range(population_size):
        Chromosome()
    Chromosome.sort_population()

def get_voyage():
    return (0, [])

def main() -> None:
    start_time = time.time()
    generate_initial_population()
    print(tuple(i.distance for i in Chromosome.population))
    print(Chromosome.total_distance)
    distance, road = get_voyage()
    end = time.time() - start_time
    print(json.dumps({"distance": distance, "road": road, "time": end}))


if __name__ == "__main__":
    debug = True
    matrix = get_distance_matrix()
    population_size = matrix.shape[0]
    no_mutation_elite_chromosomes = 0
    main()