import matplotlib.pyplot as plt
import numpy as np
import os

def plot(file, plot = False, plot_bar = False, name = None, x_name = None,x_lim = None, y_name = None, width = 10, normalized = False):
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
        if x_lim:
            plt.xlim(x_lim[0], x_lim[1])
        plt.ylabel(y_name)
        plt.legend()
        plt.show()
    return name, x, y

def int_dif(file_a, file_b, target_energy):
    """
    Calculate the absolute difference between intensities in two data arrays at the closest energy value to target_energy.
    """
    # Find the index of the closest energy value to target_energy in both arrays
    a = np.abs(file_a[:, 0] - target_energy).argmin()
    b = np.abs(file_b[:, 0] - target_energy).argmin()
    
    # Calculate the absolute difference between the intensities
    dif = np.abs(file_a[a, 1] - file_b[b, 1])
    
    return dif