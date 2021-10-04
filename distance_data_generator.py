#!/usr/bin/env python3

__author__ = "Ashot Vantsyan"
__copyright__ = "Copyright (c) 2020, Diploma project"
__version__ = "0.1.1"
__maintainer__ = "Ashot Vantsyan"
__email__ = "ashotvantsyan@gmail.com"
__status__ = "Dev"

import os
import numpy as np
from distance_generator import generate_distance

def generate_data_directory_structure():
    for i in range(0, 1000000, 100000):
        start, end = i, i + 99999
        i000000_directory = directory = os.path.join("input_data", f"{start}-{end}")
        if not os.path.isdir(directory):
            os.makedirs(directory)
        for j in range(0, 100000, 10000):
            start, end = j, j + 9999
            i00000_directory = os.path.join(i000000_directory, f"{start}-{end}")
            directory = os.path.join(i000000_directory, f"{start}-{end}")
            if not os.path.isdir(directory):
                os.makedirs(directory)
            for k in range(0, 10000, 1000):
                start, end = k, k + 999
                i0000_directory = os.path.join(i00000_directory, f"{start}-{end}")
                directory = os.path.join(i00000_directory, f"{start}-{end}")
                if not os.path.isdir(directory):
                    os.makedirs(directory)
                for l in range(0, 1000, 100):
                    start, end = l, l + 99
                    i000_directory = os.path.join(i0000_directory, f"{start}-{end}")
                    directory = os.path.join(i0000_directory, f"{start}-{end}")
                    if not os.path.isdir(directory):
                        os.makedirs(directory)
                    for m in range(0, 100, 10):
                        start, end = m, m + 9
                        directory = os.path.join(i000_directory, f"{start}-{end}")
                        if not os.path.isdir(directory):
                            os.makedirs(directory)

def main() -> None:
    generate_data_directory_structure()
    for i in range(4, 1000):
        digits = "0" * (6 - len(str(i))) + str(i)
        file = os.path.join(
            "input_data",
            f"{int(digits[0]) * 100000}-{int(digits[0]) * 100000 + 99999}",
            f"{int(digits[1]) * 10000}-{int(digits[1]) * 10000 + 9999}",
            f"{int(digits[2]) * 1000}-{int(digits[2]) * 1000 + 999}",
            f"{int(digits[3]) * 100}-{int(digits[3]) * 100 + 99}",
            f"{int(digits[4]) * 10}-{int(digits[4]) * 10 + 9}",
            f"{i}_city_distances.csv"
        )
        if not os.path.isfile(file):
            generate_distance(i, file, 1, 10 ** len(str(i)))
        if not os.path.isdir("analysis"):
            os.makedirs("analysis")

if __name__ == "__main__":
    main()