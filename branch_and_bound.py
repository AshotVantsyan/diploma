#!/usr/bin/env python3

__author__ = "Ashot Vantsyan"
__copyright__ = "Copyright (c) 2020, Diploma project"
__version__ = "0.2"
__maintainer__ = "Ashot Vantsyan"
__email__ = "ashotvantsyan@gmail.com"
__status__ = "Dev"

import numpy as np
from typing import Optional

def get_distance_matrix() -> np.matrix:
    matrix = np.loadtxt("city_distances.csv", delimiter=",")
    return np.matrix(matrix)

def get_matrix_cost(matrix: np.matrix, debug=False) -> tuple:
    matrix_mod = matrix.copy()
    minimal_column = matrix.min(1)[np.newaxis].T
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
    return cost, matrix_mod

class Tree:

    def __init__(self, node_name: int, matrix: Optional[np.matrix] = None, parent: Optional['Tree'] = None) -> None:
        self._node_name = node_name
        self._path = (self._node_name,)
        self._matrix = matrix
        self._parent = parent
        self._children = []
        if parent is None:
            self.root = self
            self._leafs = [self]
            assert isinstance(matrix, np.matrix), "You must specify initial matrix for root"
        else:
            self.root = self._parent.root
            self._path = parent._path + self._path
            self.root._leafs.append(self)
            self._parent.add_child(self)
        self._node_cost = None

    def get_path(self) -> tuple:
        return self._path

    def get_parent(self) -> Optional['Tree']:
        return self._parent

    def add_child(self, node: Optional['Tree']) -> None:
        self._children.append(node)
        if self in self.root._leafs:
            self.root._leafs.remove(self)

    def is_leaf(self, node: Optional['Tree']) -> bool:
        return self in self.root._leafs
        
    def set_cost(self) -> None:
        if self is self.root:
            self._node_cost, self._matrix = get_matrix_cost(self._matrix)
        else:
            self._node_cost, self._matrix = get_matrix_cost(self._parent._matrix)
    
    def get_leaf_with_minimal_cost(self) -> tuple:
        minimal = (self.root._leafs[0], self.root._leafs[0]._node_cost)
        for leaf in self.root._leafs[1:]:
            if leaf._node_cost < minimal[1]:
                minimal = (leaf, leaf._node_cost)
        return minimal

    def __str__(self):
        return f"<Node {self._node_name}: path - {self._path}, cost - {self._node_cost}>"

    def __repr__(self):
        return f"<Node {self._node_name}: path - {self._path}, cost - {self._node_cost}>"

    def print_node(self, debug=True) -> None:
        prefix = "  " * (len(self._path) - 1)
        print(f"{prefix}<Node {self._node_name}: path - {self._path}, cost - {self._node_cost}>")
        if debug:
            if hasattr(self, "_leafs"):
                print(f"{prefix}`-- Leafs {self._leafs}")
            print(f"{prefix}`-- Matrix")
            for line in self._matrix.__str__().splitlines():
                print(f"{prefix}-- {line}")

def get_distance(matrix, city1, city2):
    return matrix[city1, city2]

def get_minimal_voyage(matrix, roads, debug=False):
    best_road = None
    minimal_distance = None
    return best_road, minimal_distance

def main() -> None:
    matrix = get_distance_matrix()
    root = Tree(1, matrix)
    # roads = None
    # road, distance = get_minimal_voyage(matrix, roads, debug=False)
    # print(road, distance)

if __name__ == "__main__":
    main()