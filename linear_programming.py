#!/usr/bin/env python3

__author__ = "Ashot Vantsyan"
__copyright__ = "Copyright (c) 2021, Diploma project"
__version__ = "1.0"
__maintainer__ = "Ashot Vantsyan"
__email__ = "ashotvantsyan@gmail.com"
__status__ = "Released"

import os
import json
import time
import numpy as np
import pulp as lp
from typing import Iterable

def get_distance_matrix() -> np.matrix:
    file = os.getenv("DISTANCE_FILE", "city_distances.csv")
    matrix = np.loadtxt(file, delimiter=",")
    return np.matrix(matrix)

def get_distances(matrix: np.matrix) -> tuple:
    cities = range(1, matrix.shape[0] + 1)
    distances = dict(((i, j), matrix[i - 1, j - 1]) for i in cities for j in cities if i != j)
    return cities, distances

def state_problem() -> lp.LpProblem:
    return lp.LpProblem("The_Travelling_Salesman_Problem", lp.LpMinimize)
    
def define_variables_and_constraints(problem: lp.LpProblem, distances: dict, cities: Iterable):
    x = lp.LpVariable.dicts("x", distances, 0, 1, lp.LpBinary)
    problem += lp.lpSum([x[(i, j)] * distances[(i, j)] for (i, j) in distances])
    for k in cities:
        problem += lp.lpSum([x[(i, k)] for i in cities if (i, k) in x]) == 1
        problem += lp.lpSum([x[(k, i)] for i in cities if (k, i) in x]) == 1
    city_count = len(cities)
    u = lp.LpVariable.dicts('u', cities, 0, city_count-1,lp.LpInteger)
    for i in cities:
        for j in cities:
            if i != j and (i != 1 and j!= 1) and (i, j) in x:
                problem += u[i] - u[j] <= (city_count) * (1 - x[(i, j)]) - 1
    return x, u

def get_minimal_voyage(problem: lp.LpProblem, x: lp.LpVariable, cities: Iterable) -> tuple:
    problem.solve(lp.PULP_CBC_CMD(msg=0))
    distance = lp.value(problem.objective)
    start = 1
    cities_left = list(cities)
    voyage=[cities_left.pop(cities_left.index(start))]
    while len(cities_left) > 0:
        for i in cities_left:
            if x[(start, i)].varValue == 1:
                voyage.append(cities_left.pop(cities_left.index(i)))
                start=i
                break
    voyage.append(1)

    return tuple(voyage), distance

def main() -> None:
    start = time.time()
    matrix = get_distance_matrix()
    cities, distances = get_distances(matrix)
    problem = state_problem()
    x, _ = define_variables_and_constraints(problem, distances, cities)
    road, distance = get_minimal_voyage(problem, x, cities)
    end = round(time.time() - start, 2)
    print(json.dumps({"distance": distance, "road": road, "time": end}))

if __name__ == "__main__":
    main()
