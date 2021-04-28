from mpl_toolkits import mplot3d

# %matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

class Plot3D:
    def show(self):
        fig = plt.figure()
        ax = plt.axes(projection='3d')

        plt.show()
