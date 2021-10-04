#!/usr/bin/env python3

__author__ = "Ashot Vantsyan"
__copyright__ = "Copyright (c) 2020, Diploma project"
__version__ = "1.0"
__maintainer__ = "Ashot Vantsyan"
__email__ = "ashotvantsyan@gmail.com"
__status__ = "Released"

import os
import time
import json
import numpy as np

generation_count = 100

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

    @classmethod
    def get_probabilities(cls):
        proportions = np.array(tuple(cls.total_distance / chromosome.distance for chromosome in cls.population))
        coeff = 1 / np.sum(proportions)
        return tuple(proportion * coeff for proportion in proportions)

    @classmethod
    def mutate_population(cls):
        for chromosome in cls.population:
            chromosome.mutate()

    def __init__(self, road=None):
        self.road = np.array(np.random.permutation(range(matrix.shape[0])), dtype=np.int32) if road is None else road
        self.distance = get_road_distance(matrix, self.road)
        if debug and False:
            print(f"Road: {self.road}, Distance: {self.distance}")
        Chromosome.add_to_population(self)
    
    def mutate(self):
        i, j = sorted(np.random.choice(range(len(self.road)), 2, replace=False))
        self.road[i], self.road[j] = self.road[j], self.road[i]
        Chromosome.total_distance -= self.distance
        self.distance = get_road_distance(matrix, self.road)
        Chromosome.total_distance += self.distance

    def __str__(self):
        return f"<Chromosome: {self.road}, {self.distance}>"

    def __repr__(self):
        return f"<Chromosome: {self.road}, {self.distance}>"

def generate_initial_population():
    for _ in range(population_size):
        Chromosome()
    Chromosome.sort_population()

def choose_parents():
    return np.random.choice(Chromosome.population, size=2, p=Chromosome.get_probabilities())

def array_index(array, index):
    return np.where(array == index)[0][0]

def crossover(parent1, parent2):
    offspring1, offspring2 = np.empty(parent1.shape, dtype=np.int32), np.empty(parent2.shape, dtype=np.int32)
    offspring1.fill(-1)
    offspring2.fill(-1)
    next_position = 0
    for _ in range(parent1.shape[0]):
        if parent1[next_position] in offspring1:
            break
        offspring1[next_position] = parent1[next_position]
        next_position = array_index(parent1, parent2[next_position])
    for i in range(parent1.shape[0]):
        if offspring1[i] == -1:
            offspring1[i] = parent2[i]
    next_position = 0
    for _ in range(parent2.shape[0]):
        if parent2[next_position] in offspring2:
            break
        offspring2[next_position] = parent2[next_position]
        next_position = array_index(parent2, parent1[next_position])
    for i in range(parent2.shape[0]):
        if offspring2[i] == -1:
            offspring2[i] = parent1[i]
    return offspring1, offspring2

def generate_next_population():
    for _ in range(len(Chromosome.population) // 2):
        parents = choose_parents()
        offspring1, offspring2 = crossover(parents[0].road, parents[1].road)
        Chromosome.sort_population()
        Chromosome.remove_from_population(-2, 0)
        Chromosome(offspring1)
        Chromosome(offspring2)
        Chromosome.mutate_population()

def get_voyage():
    generate_initial_population()
    distance = np.inf
    road = []
    generation = 0
    while generation < generation_count:
        generate_next_population()
        Chromosome.sort_population()
        if Chromosome.population[0].distance < distance:
            distance = Chromosome.population[0].distance
            road = Chromosome.population[0].road
            generation = 0
        generation += 1
    road = tuple(int(i + 1) for i in tuple(map(int, road)) + (int(road[0]),))
    return int(distance), road

def main() -> None:
    start = time.time()
    distance, road = get_voyage()
    end = round(time.time() - start, 2)
    print(json.dumps({"distance": distance, "road": road, "time": end}))


if __name__ == "__main__":
    debug = False
    matrix = get_distance_matrix()
    population_size = matrix.shape[0]
    main()
