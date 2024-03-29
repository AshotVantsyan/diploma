#!/usr/bin/env python3

__author__ = "Ashot Vantsyan"
__copyright__ = "Copyright (c) 2020-2021, Diploma project"
__version__ = "1.0.8"
__maintainer__ = "Ashot Vantsyan"
__email__ = "ashotvantsyan@gmail.com"
__status__ = "Released"

import os
import sys
import time
import json
import subprocess
import numpy as np

def get_distance_matrix(file) -> np.matrix:
    matrix = np.loadtxt(file, delimiter=",")
    return np.matrix(matrix)

def get_matrix_cost(matrix: np.matrix, debug=False) -> float:
    matrix_mod = matrix.copy()
    minimal_column = matrix.min(1)[:np.newaxis]
    minimal_column[minimal_column == np.inf] = 0
    cost = np.sum(minimal_column)
    # Subtract minimal value of a row from matrix
    matrix_mod -= minimal_column
    minimal_row = matrix_mod.min(0)
    minimal_row[minimal_row == np.inf] = 0
    cost += np.sum(minimal_row)
    # Subtract minimal value of a column from matrix
    matrix_mod -= minimal_row
    if debug:
        print(f"Minimal column: {minimal_column}")
        print(f"Minimal column cost: {np.sum(minimal_column)}")
        print(f"Minimal row: {minimal_row}")
        print(f"Minimal row cost: {np.sum(minimal_row)}")
    return float(cost)

def main() -> None:
    exact_methods = ("brute_force", "branch_and_bound", "dynamic_programming", "linear_programming")
    approx_methods = ("simulated_annealing", "nearest_neighbor", "random_choice", "ant_colony", "genetic", "rnn")
    message = "Methods:\n"
    for number, method in enumerate(exact_methods + approx_methods, start=1):
        message += f"{number}: {method.replace('_', ' ').capitalize()}\n"
    message += "Select: "
    method = int(input(message))
    assert method in range(1, len(exact_methods) + len(approx_methods) + 1), "Incorrect choice"
    method = (exact_methods + approx_methods)[method-1]
    results_file = open(os.path.join("analysis", f"{method}.csv"), "w")
    results_file.write("NumberOfCities,Time,Accuracy,Distance\n")
    results_file.close()
    for root, _, files in sorted(os.walk("input_data")):
        for file in sorted(files):
            myenv = os.environ.copy()
            myenv['DISTANCE_FILE'] = os.path.join(root, file)
            try:
                start_time = time.time()
                command = subprocess.run((sys.executable, f'{method}.py'), stdout=subprocess.PIPE, env=myenv, timeout=480)
                end_time = time.time() - start_time
                results = json.loads(command.stdout)
                number_of_cities = len(results["road"]) - 1
                distance = results["distance"]
                if hasattr(results, "time"):
                    end_time = results["time"]
                if method in exact_methods:
                    accuracy = "100%"
                else:
                    matrix = get_distance_matrix(myenv['DISTANCE_FILE'])
                    print(get_matrix_cost(matrix))
                    accuracy = "%s%%" % (get_matrix_cost(matrix) / distance * 100)
                with open(os.path.join("analysis", f"{method}.csv"), "a") as results_file:
                    results_file.write(f"{number_of_cities},{end_time},{accuracy},\"{distance}\"\n")
            except subprocess.TimeoutExpired:
                print(f"The last checked file is: {file}")
                results_file.close()
                sys.exit(0)
    results_file.close()

if __name__ == "__main__":
    main()