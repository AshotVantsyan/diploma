#!/usr/bin/env python3

__author__ = "Ashot Vantsyan"
__copyright__ = "Copyright (c) 2020, Diploma project"
__version__ = "0.3"
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
    return cost, matrix_mod

class Tree:

    def __init__(self, node_name: int, matrix: Optional[np.matrix] = None, parent: Optional['Tree'] = None) -> None:
        self.name = node_name
        self._parent = parent
        self._children = []
        self._node_cost = None
        if parent is None:
            self.root = self
            self._matrix = matrix
            self._path = (self.name,)
            self._leafs = [self]
            assert isinstance(matrix, np.matrix), "You must specify initial matrix for root"
        else:
            self.root = self.get_parent().root
            self._path = parent._path + (self.name,)
            assert not isinstance(matrix, np.matrix), "You must not specify initial matrix for non-root"
            self.root._leafs.append(self)
            self.get_parent().add_child(self)
        self.set_cost()

    def get_path(self) -> tuple:
        return self._path

    def get_parent(self) -> Optional['Tree']:
        return self._parent

    def get_matrix(self) -> np.matrix:
        return self._matrix.copy()

    def add_child(self, node: Optional['Tree']) -> None:
        self._children.append(node)
        if self in self.root._leafs:
            self.root._leafs.remove(self)

    def generate_next_node(self) -> Optional['Tree']:
        available_nodes = sorted(tuple(set(range(1, self._matrix.shape[0]+1)) - set(self._path) - set((child.name for child in self._children))))
        if available_nodes:
            return Tree(available_nodes[0], parent=self)
        return None
    
    def generate_child_nodes(self) -> None:
        while self.generate_next_node() is not None:
            pass
        
    def set_cost(self) -> None:
        if self is self.root:
            matrix = self.get_matrix()
            self._node_cost, self._matrix = get_matrix_cost(matrix)
        else:
            matrix = self.get_parent().get_matrix()
            edge_cost = matrix[self.get_parent().name-1, self.name-1]
            # Get nodes of the last edge and make corresponding row/column infinite
            matrix[self.get_parent().name-1] = np.inf
            matrix[:,self.name-1] = np.inf
            matrix[self.name-1, self.get_parent().name-1] = np.inf
            matrix[self.name-1, self.root.name-1] = np.inf
            node_cost, self._matrix = get_matrix_cost(matrix)
            self._node_cost = node_cost + edge_cost + self.get_parent()._node_cost

    
    def get_leaf_with_minimal_cost(self) -> tuple:
        minimal = (self.root._leafs[0], self.root._leafs[0]._node_cost)
        for leaf in self.root._leafs[1:]:
            if leaf._node_cost < minimal[1]:
                minimal = (leaf, leaf._node_cost)
        return minimal

    def __str__(self):
        return f"<Node {self.name}: path - {self._path}, cost - {self._node_cost}>"

    def __repr__(self):
        return f"<Node {self.name}: path - {self._path}, cost - {self._node_cost}>"

    def print_node(self, debug=False) -> None:
        prefix = "  " * (len(self._path) - 1)
        print(f"{prefix}<Node {self.name}: path - {self._path}, cost - {self._node_cost}>")
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
    root = Tree(1, matrix)
    node = root
    while len(node.get_path()) < matrix.shape[0]:
        node.generate_child_nodes()
        node, minimal_distance = root.get_leaf_with_minimal_cost()
        best_road = node._path + (node._path[0],)
    return best_road, minimal_distance

def main() -> None:
    matrix = get_distance_matrix()
    roads = None
    road, distance = get_minimal_voyage(matrix, roads, debug=False)
    print(road, distance)

if __name__ == "__main__":
    main()