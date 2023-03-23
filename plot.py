"""
File used for plotting, contains transformer and plot function
"""
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

def maze_transform(maze, path):
    """
    Transform the maze for coloring.
    We want to map the maze symbols to integers e.g. "#" -> 2, to make it 
    easier to manipulate with numpy. We are going to use numpy unique function.
    https://numpy.org/doc/stable/reference/generated/numpy.unique.html
    Numpy unique function returns the unique elements of array, with return_inverse
    we can get the indices of unique values and use this as map with integers.
    Reshape the returned flattened indice array with original maze shape.
    """
    GREEN_COLOR = 4
    # save shape for later use
    maze_shape = maze.shape

    a = np.unique(maze, return_inverse=True)[1]
    a = a.reshape(maze_shape)

    # Draw path to goal in green
    for p in path:
        x, y = p
        if a[x][y] == 0:
            a[x][y] = GREEN_COLOR
    return a


def plot_maze(maze, path):
    """
    Plot the maze with matplotlib library by utilizing
    color mapping for maze representation. Create bins for color mapping
    from 0-5 with interval of 1, where n-th bin will be mapped to the n-th color.
    """
    bins = [0, 1, 2, 3, 4, 5]
    cmap = colors.ListedColormap(["silver", "black", "red", "gold", "green"])
    norm = colors.BoundaryNorm(bins, cmap.N)

    steps = len(path)
    fig, ax = plt.subplots()
    ax.set_axis_off()
    transformed_maze = maze_transform(maze, path)
    ax.imshow(transformed_maze, cmap=cmap, norm=norm)
    # if path exists, there is a shortest path
    if path:
        ax.set_title(f"Found shortest path for Pentti, steps: {steps}")
    else:
        ax.set_title("No shortest path found to exit")

    plt.show()
