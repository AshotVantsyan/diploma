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

def generate_distance(number_of_cities: int) -> None:
    matrix = np.random.uniform(1, 101, (number_of_cities, number_of_cities))
    matrix = (matrix + matrix.T) // 2
    np.fill_diagonal(matrix, np.inf)
    np.savetxt("city_distances.csv", matrix, delimiter=',')

def main() -> None:
    number_of_cities = int(input("Please enter city count:"))
    generate_distance(number_of_cities)

if __name__ == "__main__":
    main()