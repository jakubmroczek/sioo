# from mpl_toolkits import mplot3d

import numpy as np
import matplotlib.pyplot as plt

class Plot3D:
    def f(self, x, y, function):        
        Z = []
        for a, b in zip(x, y):
            local = []
            for c, d in zip(a, b):
                local.append(function.evaluate([c, d]))
            Z.append(local)
        # Z = np.sin(np.sqrt(x ** 2 + y ** 2))
        return np.array(Z)

    # def f(self, X, Y, function):
    #     z = np.array([[1, 2], [2, 2], [3, 4]])
    #     # TODO: Poor cartesian product xD
    #     for x in X:
    #         for y in Y:
    #             np.append(z, function.evaluate((x, y)))
    #     print(z)
    #     return z

    def show(self, result):
        #TODO: this must be adujsted to initial serach point
        x = np.linspace(-6, 6, 30)
        y = np.linspace(-6, 6, 30)
        
        X, Y = np.meshgrid(x, y)

        Z = self.f(X, Y, result.function)
        # print(Z.shape)

        fig = plt.figure()
        ax = plt.axes(projection='3d')
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                cmap='viridis', edgecolor='none')
        ax.set_title('surface');

        plt.show()
