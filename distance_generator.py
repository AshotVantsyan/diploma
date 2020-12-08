#!/usr/bin/env python3

import pickle
import numpy as np

def main() -> None:
    number_of_cities = int(input("Please enter city count:"))
    matrix = np.random.randint(1, 101, size=(number_of_cities, number_of_cities))
    matrix = (matrix + matrix.T) // 2
    np.fill_diagonal(matrix, 0)
    np.savetxt("city_distances.csv", matrix, delimiter=',')

if __name__ == "__main__":
    main()