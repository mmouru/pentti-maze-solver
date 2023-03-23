"""
Main file to run the maze solver, to run the maze solver run $python main.py <maze-file-location>
This solver works for any sized ( atleast rectangular ) maze.
Contains queue, value classes and pentti class to solve given maze problem. This implementation
uses pandas to ease txt file reading and numpy packages to ease working with arrays.
"""
import sys
import pandas as pd
import numpy as np
from plot import plot_maze


class Value:
    """
    Value represents a singular node that is used for graph search and
    tracking the path of Pentti. Value includes has spatial information
    of node and parent if given. For root node parent is None.
    """

    def __init__(self, point, parent=None):
        self.point = point
        self.parent = parent

    def get_parent(self):
        """
        Returns parent node if present
        """
        return self.parent


class Queue:
    """
    Simple FIFO queue to be used in graph search. Root node is given by Pentti
    """

    def __init__(self, root):
        self.values = [Value(root)]

    def dequeue(self):
        """
        Return first node in queue with array slicing
        """
        try:
            value = self.values[:1]
            self.values = self.values[1:]
            return value[0]
        except IndexError:
            return "No nodes to dequeue"

    def enqueue(self, val):
        """
        Set node to back of queue
        """
        self.values = self.values + [val]

    def is_empty(self):
        """
        To check if queue has any nodes left
        """
        if len(self.values) > 0:
            return False
        return True


class Pentti:
    """
    Pentti class
    """

    def __init__(self, start=(0, 0), steps=20):
        self.start = start
        self.maze = None
        self.solved = False
        self.exit = []
        self.path = []
        self.steps = steps

    def set_maze_from_file(self, txt_file=None):
        """
        Set maze from txt_file
        """
        list_for_maze = pd.read_csv(txt_file, header=None)[0].tolist()
        self._set_maze_exit_start(list_for_maze)

    def set_maze(self, maze):
        """
        Set maze as 2D matrix
        """
        self._set_maze_exit_start(maze)
        self.maze = np.array(maze)

    def _get_adjacent_edges(self, value):
        """
        Get adjacent edges to coordinate value, out-of-boundary checks are done
        in BFS implementation
        """
        x, y = value.point
        return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

    def _set_maze_exit_start(self, maze):
        """
        Set maze, exit and start values for Pentti
        """
        for i, lista in enumerate(maze):
            maze[i] = [*lista]

        # turn to np array for easier manipulation
        maze = np.array(maze)
        # find indices for exits
        exits = np.argwhere(maze == "E")
        self.exit = [(idx[0], idx[1]) for idx in exits]
        self.maze = maze
        # find indice for start
        idx = np.argwhere(maze == "^")[0]
        self.start = (idx[0], idx[1])

    def solve_maze(self):
        """
        Breadt-first-search solution to solve path to closest exit, if one exists in maze.
        If many exits exist, BFS automatically returns the optimal one.
        Pseudo-code for implementation can be found in:
        https://en.wikipedia.org/wiki/Breadth-first_search#Pseudocode
        Returns True/False depending if exit is found for Pentti.
        """
        visited = Queue(self.start)
        q = Queue(self.start)
        backtrack = Queue(self.start)  # To save all values for backtracking

        while not q.is_empty():
            v = q.dequeue()
            if v.point in self.exit:
                self._path(backtrack.values)
                return True
            adjacent_edges = self._get_adjacent_edges(v)
            for edge in adjacent_edges:
                try:
                    val = self.maze[edge[0]][edge[1]]
                    if val != "#" and edge not in visited.values:
                        visited.enqueue(edge)
                        new_val = Value(edge, parent=v)
                        q.enqueue(new_val)
                        backtrack.enqueue(new_val)

                # Out of bounds skip
                except IndexError:
                    pass
        return False
    
    def _path(self, track):
        """
        Backtrack the optimal path for Pentti to exit the maze.
        Easy recursive backtracking can be implemented with Value class
        until no parent is found in root node.
        """
        # exit is the last value in track
        exit = track.pop()

        def recursive_path_finder(value):
            """
            Recursively build path from nodes parent until no parent is found ( start )
            """
            self.path.append(value.point)
            if value.parent:
                recursive_path_finder(value.parent)

        recursive_path_finder(exit)


if __name__ == "__main__":
    pentti = Pentti()
    pentti.set_maze_from_file(sys.argv[1])
    pentti.solve_maze()

    plot_maze(pentti.maze, pentti.path)
