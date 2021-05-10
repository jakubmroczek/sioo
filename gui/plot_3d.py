import numpy as np
import matplotlib.pyplot as plt

class Plot3D:
    def show(self, result):
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        
        self._plot_function_surface(result, ax)
        self._plot_intermediate_steps(result, ax)
        
        # TODO: Rename the title
        ax.set_title('surface');
        
        plt.show()

    def _plot_function_surface(self, result, ax):
        #TODO: this must be adujsted to initial serach point
        x = np.linspace(-6, 6, 30)
        y = np.linspace(-6, 6, 30)
        
        X, Y = np.meshgrid(x, y)

        Z = self._function_at_xy(X, Y, result.function)
        
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                cmap='viridis', edgecolor='none')
        
    def _plot_intermediate_steps(self, result, ax):
        xs = [1,  2 , 43, 4]
        ys = [1,  2 , 43, 4]
        zs = [1,  2 , 43, 4]
        ax.scatter(xs, ys, zs, marker='x')

    def _function_at_xy(self, x, y, function):        
            Z = []
            for a, b in zip(x, y):
                local = []
                for c, d in zip(a, b):
                    local.append(function.evaluate([c, d]))
                Z.append(local)
            return np.array(Z)    