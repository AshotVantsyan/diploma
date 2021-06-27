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
import multiprocessing
import numpy as np

distance_coeff = 8
pheromone_coeff = 8
evaporation_coeff = 0.80
generation_count = 5
initial_pheromone = 2

def get_distance_matrix() -> np.matrix:
    file = os.getenv("DISTANCE_FILE", "city_distances.csv")
    matrix = np.loadtxt(file, delimiter=",")
    return np.matrix(matrix)

def get_pheromone_matrix(matrix: np.matrix) -> np.matrix:
    pheromone = get_matrix_cost(matrix)
    pheromone[pheromone != 0] = initial_pheromone 
    pheromone[pheromone == 0] = initial_pheromone * 2
    np.fill_diagonal(pheromone, 0)
    return pheromone

def get_matrix_cost(matrix: np.matrix) -> np.matrix:
    cost_matrix = matrix.copy()
    minimal_column = matrix.min(1)[:np.newaxis]
    minimal_column[minimal_column == np.inf] = 0
    # Subtract minimal value of a row from matrix
    cost_matrix -= minimal_column
    minimal_row = cost_matrix.min(0)
    minimal_row[minimal_row == np.inf] = 0
    # Subtract minimal value of a column from matrix
    cost_matrix -= minimal_row
    return cost_matrix

distance = get_distance_matrix()
reciprocal = np.reciprocal(distance)
pheromone = get_pheromone_matrix(distance)
ant_count = city_count = pheromone_effect = distance.shape[0]

def evaporate_pheromone(matrix: np.matrix) -> None:
    matrix *= evaporation_coeff

class Ant:

    _pheromone = pheromone
    _pheromone_coeff = pheromone_coeff
    _reciprocal = reciprocal
    _distance = distance
    _distance_coeff = distance_coeff

    def __init__(self):
        self.path = []
        self.path_length = 0
        self.start_city = self.current_city = np.random.randint(0, city_count)
        self.available_cities = list(range(city_count))
        self.available_cities.remove(self.current_city)
    
    def get_probabilities(self):
        city_probabilities = []
        for i in range(len(self.available_cities)):
            city_probabilities.append(
                (self._pheromone[self.current_city, self.available_cities[i]] ** self._pheromone_coeff) * \
                (self._reciprocal[self.current_city, self.available_cities[i]] ** self._distance_coeff)
            )
        probabilities = np.ndarray((3, len(self.available_cities)))
        sum_city_probabilies = sum(city_probabilities)
        for i in range(len(self.available_cities)):
            probabilities[0, i] = self.current_city
            probabilities[1, i] = self.available_cities[i]
            probabilities[2, i] = city_probabilities[i] / sum_city_probabilies
        return probabilities
    
    def make_choice(self):
        probabilities = self.get_probabilities()
        choice = np.random.choice(len(self.available_cities), p=probabilities[2])
        return probabilities[:, choice]

    def pave_way(self, debug=False):
        while len(self.available_cities) != 0:
            from_city, to_city, _ = map(int, self.make_choice())
            self.path.append((from_city, to_city))
            self.path_length += self._distance[from_city, to_city]
            self.available_cities.remove(to_city)
            self.current_city = to_city
            if debug:
                print(f"Choice: {to_city}, Length: {self.path_length}, Path: {self.path}, Available Cities: {self.available_cities}")
        self.path.append((self.current_city, self.start_city))
        self.path_length += self._distance[self.current_city, self.start_city]
        if debug:
            print(f"Length: {self.path_length}, Path: {self.path}, Available Cities: {self.available_cities}")

def pave_colony_way(ant: Ant) -> Ant:
    ant.pave_way()
    return ant
    
def get_one_ant_colony_generation_optimized_voyage():
    distance = np.inf
    ants = (Ant() for _ in range(ant_count))
    with multiprocessing.Pool() as pool:
        ants = pool.map(func=pave_colony_way, iterable=ants)
        pool.close()
        pool.join()
    evaporate_pheromone(pheromone)
    for ant in ants:
        for i, j in ant.path:
            pheromone[i, j] += pheromone_effect / ant.path_length
        if distance > ant.path_length:
            distance = ant.path_length
            road = tuple(i+1 for i, _ in ant.path) + (ant.path[0][0]+1,)
    return road, distance

def main() -> None:
    distance = np.inf
    generation = generation_count
    start_time = time.time()
    while generation != 0:
        new_road, new_distance = get_one_ant_colony_generation_optimized_voyage()
        if distance > new_distance:
            road, distance = new_road, new_distance
            generation = generation_count
        else:
            generation -= 1
    end = round(time.time() - start_time, 2)
    print(json.dumps({"distance": distance, "road": road, "time": end}))


if __name__ == "__main__":
    main()
