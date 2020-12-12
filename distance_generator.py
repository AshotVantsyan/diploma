#!/usr/bin/env python3

__author__ = "Ashot Vantsyan"
__copyright__ = "Copyright (c) 2020, Diploma project"
__version__ = "0.1"
__maintainer__ = "Ashot Vantsyan"
__email__ = "ashotvantsyan@gmail.com"
__status__ = "Dev"

import numpy as np

def generate_distance(number_of_cities: int) -> None:
    matrix = np.random.randint(1, 101, size=(number_of_cities, number_of_cities))
    matrix = (matrix + matrix.T) // 2
    np.fill_diagonal(matrix, 0)
    np.savetxt("city_distances.csv", matrix, delimiter=',')

def main() -> None:
    number_of_cities = int(input("Please enter city count:"))
    generate_distance(number_of_cities)

if __name__ == "__main__":
    main()