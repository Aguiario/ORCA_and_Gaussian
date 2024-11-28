import matplotlib.pyplot as plt
import numpy as np
import os

def ORCA_plot(file, plot = False, name = None, x = None, y = None, bar_width = 10):
    x, y = file[:, 0], file[:, 1]

    if plot == True:
        plt.figure(figsize=(10, 6))
        plt.bar(x, y, width=bar_width, label=name, alpha=0.6)
        plt.xlabel(x)
        plt.ylabel(y)
        plt.legend()
        plt.show()
    return name, x, y