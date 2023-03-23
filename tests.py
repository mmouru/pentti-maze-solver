"""
Test file for solver, tests all classes and transformer function from plot file.
"""
import numpy as np
import pytest
from main import Value, Queue, Pentti
from plot import maze_transform

test_point = (5, 6)

# 6x7 test mazes
test_maze_1 = [
    ["#", "#", "#", "#", "#", "E", "#"],
    ["#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", " ", "#", "#", " ", "#"],
    ["#", "#", " ", " ", " ", " ", "#"],
    ["#", "#", " ", " ", " ", "#", "#"],
    ["#", "#", "^", "#", "#", "#", "#"],
]

test_maze_2 = [
    ["#", "#", "#", "E", "#", "E", "#"],
    ["#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", "#", "#", " ", "#"],
    ["#", "#", " ", " ", " ", " ", "#"],
    ["#", "#", " ", " ", " ", "#", "#"],
    ["#", "#", "^", "#", "#", "#", "#"],
]
test_exit = [(0, 5)]  # there can be many exits
test_start = (5, 2)


def test_value_class():
    """
    Root value node can be created without parent node.
    Value node can be created with parent and the parent is presented.
    """

    test_val = Value(test_point)
    assert test_val.point == test_point
    assert test_val.get_parent() == None
    second_test_val = Value((6, 6), test_val)
    assert second_test_val.parent == test_val


def test_queue_class():
    """
    Nodes can be added and removed from queue, Queue cant be created
    without root, dequeue returns first element, not last added, cant
    remove items from empty queue
    """
    test_value = Value(test_point)
    queue = Queue(test_value)
    queue.enqueue(Value((6, 6)))
    value = queue.dequeue().point
    assert value.point == test_point
    # queue should return false if nodes are present
    assert queue.is_empty() == False
    queue.dequeue()
    assert queue.is_empty() == True
    assert queue.dequeue() == "No nodes to dequeue"
    with pytest.raises(TypeError):
        Queue()


def test_pentti_class():
    """
    Pentti can be created and maze can be set from 2D arr,
    setting maze sets starting point and exits, maze can be solved
    if path exists for exit, and maze cant be solved if no path
    exists.
    """
    pentti = Pentti()
    pentti.set_maze(test_maze_1)
    assert pentti.start == test_start
    assert pentti.exit == test_exit

    found_path = pentti.solve_maze()
    assert found_path == True

    # Set maze with no path to exit
    pentti.set_maze(test_maze_2)
    # two exits are found
    assert len(pentti.exit) == 2
    # no found path returns False
    assert pentti.solve_maze() == False


def test_plotting():
    """
    Assert that shape stays constant during transformation.
    Assert values are changed to what they are suppose to change
    Including the path value (4) is added if founded
    """
    pentti = Pentti()
    pentti.set_maze(test_maze_1)
    shape = np.array(test_maze_1).shape
    pentti.solve_maze()
    transformed_maze = maze_transform(pentti.maze, pentti.path)
    assert transformed_maze.shape == shape

    assert transformed_maze[0][0] == 1
    assert transformed_maze[1][1] == 0
    x, y = test_start
    assert transformed_maze[x][y] == 3
    x, y = test_exit[0]
    assert transformed_maze[x][y] == 2
