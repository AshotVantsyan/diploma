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

# Constants
beta = 1e-2
current_iter = 0
iter_step = 1e-2
eta = 1e1
lamda = 1e2
tau = 1e2
probability_coeff = 1 << 4
epsilon = 0
stabilization_rate = 1e-2
stabilization_iterations = 20

def get_distance_matrix() -> np.matrix:
    file = os.getenv("DISTANCE_FILE", "city_distances.csv")
    matrix = np.loadtxt(file, delimiter=",")
    return np.matrix(matrix)

def get_recurrent_neural_network_matrix(matrix: np.matrix) -> np.matrix:
    matrix = np.random.uniform(low=-0.5, high=0.5, size=matrix.shape)
    return np.matrix(matrix)

def get_solution_matrix(rnn_matrix: np.matrix) -> np.matrix:
    matrix = np.empty(rnn_matrix.shape)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            rnn_cell = rnn_matrix[i, j] if j != starting_point else probability_coeff * rnn_matrix[i, j]
            matrix[i, j] = 1.0 / (1 + np.exp(-beta*rnn_cell))
    return matrix

def get_next_rnn_matrix(rnn_matrix: np.matrix, distance_matrix: np.matrix, solution_matrix: np.matrix) -> np.matrix:
    global epsilon
    matrix = rnn_matrix.copy()
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            epsilon = (np.sum(solution_matrix[:, i]) + np.sum(solution_matrix[:, j]) - 2)
            matrix[i, j] = matrix[i, j] - iter_step * (eta * epsilon) + (lamda * (distance_matrix[i, j] * np.exp(-current_iter / tau)))
    return matrix

def transform_solution_matrix_and_get_distance(matrix: np.matrix, distance_matrix: np.matrix) -> tuple:
    i_start = i = np.random.randint(0, matrix.shape[0]-1)
    j_max = -1
    distance = 0
    road = [i]
    length = 0
    while length < matrix.shape[0]:
        j_max = np.where(matrix[i] == np.max(matrix[i]))[-1][0]
        if i_start == j_max and length + 1 < matrix.shape[0]:
            matrix[i, j_max] = 0
            continue
        matrix[i] = np.zeros(matrix.shape[0])
        matrix[:, j_max] = np.array(np.zeros(matrix.shape[0])).T
        matrix[i, j_max] = 1
        distance += distance_matrix[i, j_max]
        road.append(j_max)
        i = j_max
        length += 1
    return road, distance

def get_road_distance(road, distance_matrix):
    distance = 0
    for i in range(len(road)):
        distance += distance_matrix[road[i-1], road[i]]
    return distance

def cost_change(distance_matrix, n1, n2, n3, n4):
    return distance_matrix[n1, n3] + distance_matrix[n2, n4] - distance_matrix[n1, n2] - distance_matrix[n3, n4]

def perform_2_opt_optimization(road: list, distance_matrix: np.matrix) -> tuple:
    new_road = road
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
    distance = get_road_distance(new_road, distance_matrix)
    road = tuple(int(i + 1) for i in new_road)
    return road, distance

def get_voyage(distance_matrix: np.matrix) -> tuple:
    global current_iter, starting_point
    recurrent_neural_network_matrix = get_recurrent_neural_network_matrix(distance_matrix)
    starting_point = np.where(recurrent_neural_network_matrix[0] == np.max(recurrent_neural_network_matrix[0]))[-1][0]
    solution_matrix = get_solution_matrix(recurrent_neural_network_matrix)
    i = 0
    while i < stabilization_iterations:
        recurrent_neural_network_matrix = get_next_rnn_matrix(recurrent_neural_network_matrix, distance_matrix, solution_matrix)
        old_epsilon = epsilon
        solution_matrix = get_solution_matrix(recurrent_neural_network_matrix)
        current_iter += iter_step
        if abs(old_epsilon - epsilon) > stabilization_rate:
            i = 0
        i += 1
    road, distance = transform_solution_matrix_and_get_distance(solution_matrix, distance_matrix)
    road, distance = perform_2_opt_optimization(road, distance_matrix)
    return road, distance

def main() -> None:
    start = time.time()
    distance_matrix = get_distance_matrix()
    np.fill_diagonal(distance_matrix, 0)
    road, distance = get_voyage(distance_matrix)
    end = round(time.time() - start, 2)
    print(json.dumps({"distance": distance, "road": road, "time": end}))

if __name__ == "__main__":
    main()
