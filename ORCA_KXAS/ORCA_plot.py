import matplotlib.pyplot as plt
import numpy as np
import os

def plot(file, plot = False, plot_bar = False, name = None, x_name = None,x_lim = None, y_name = None, width = 10, normalized = False, **kwargs):
    """
    This function, `plot`, is designed to plot data from a given file using either a line plot or a bar 
    plot, or both, based on the provided arguments.
    
    Returns:
    - name: The label name for the plot.
    - x: The x-axis data.
    - y: The  y-axis data.
    """

    x, y = file[:, 0], file[:, 1]

    if normalized:
        y = (y - np.min(y)) / (np.max(y) - np.min(y))

    if plot:
        plt.figure(figsize=(10, 6))
        plt.plot(x, y,linewidth=width ,label=name, alpha=0.6)
        plt.xlabel(x_name)
        plt.xlim(x_lim[0], x_lim[1])
        plt.ylabel(y_name)
        plt.legend()
        plt.show()

    if plot_bar:
        plt.figure(figsize=(10, 6))
        plt.bar(x, y, width=width, label=name, alpha=0.6)
        plt.xlabel(x_name)
        plt.xlim(x_lim[0], x_lim[1])
        plt.ylabel(y_name)
        plt.legend()
        plt.show()
    return name, x, y