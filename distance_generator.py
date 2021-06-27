#!/usr/bin/env python3

__author__ = "Ashot Vantsyan"
__copyright__ = "Copyright (c) 2020, Diploma project"
__version__ = "0.1.1"
__maintainer__ = "Ashot Vantsyan"
__email__ = "ashotvantsyan@gmail.com"
__status__ = "Dev"

import numpy as np

# TODO: make another function which gets distance matrix from coordinates
# Things to consider:
# # Compute distance matrix
#    dist = np.ceil(np.sqrt ((X.reshape(n,1) - X.reshape(1,n))**2 +
#                            (Y.reshape(n,1) - Y.reshape(1,n))**2))

def generate_distance_old(number_of_cities: int, file: str = "city_distances.csv", start: int = 1, end: int = 101) -> None:
    matrix = np.random.uniform(start, end, (number_of_cities, number_of_cities))
    matrix = (matrix + matrix.T) // 2
    np.fill_diagonal(matrix, np.inf)
    np.savetxt(file, matrix, delimiter=',')

def generate_distance(number_of_cities: int, file: str = "city_distances.csv", start: int = 1, end: int = 101):
    x_coords = np.random.uniform(start, end, (1, number_of_cities))
    y_coords = np.random.uniform(start, end, (1, number_of_cities))
    matrix = np.sqrt((x_coords.reshape(number_of_cities, 1) - x_coords.reshape(1, number_of_cities))**2 +
                              (y_coords.reshape(number_of_cities, 1) - y_coords.reshape(1, number_of_cities))**2)
    np.savetxt("city_x_coords.csv", x_coords, delimiter=',')
    np.savetxt("city_y_coords.csv", y_coords, delimiter=',')
    np.fill_diagonal(matrix, np.inf)
    np.savetxt(file, matrix, delimiter=',')

def main() -> None:
    number_of_cities = int(input("Please enter city count:"))
    generate_distance(number_of_cities)

if __name__ == "__main__":
    main()