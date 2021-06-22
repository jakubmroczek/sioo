import numpy as np
import matplotlib.pyplot as plt

class Plot3D:
    def show(self, result):
        fig = plt.figure(figsize=(10, 10))
        ax = plt.axes(projection='3d')
        
        self._plot_intermediate_steps(result, ax)
        self._plot_function_surface(result, ax)
        self._plot_optimum_place(result, ax)

        fig.canvas.set_window_title('Wykres funkcji')

        plt.show()

    def _plot_function_surface(self, result, ax):
        #TODO: this must be adujsted to initial serach point
        x = np.linspace(-6, 6, 30)
        y = np.linspace(-6, 6, 30)
        
        X, Y = np.meshgrid(x, y)

        Z = self._function_at_xy(X, Y, result.function)
        
        ax.plot_wireframe(X, Y, Z, color='black')
        
    def _plot_intermediate_steps(self, result, ax):
        # Coordinates of the points on the scatter grid
        xs, ys, zs = [], [], []

        for i in range(0, len(result.search_history) - 1):
            step = result.search_history[i]
            print('THIS IS A STEP MAN')
            print(step)
            xs.append(step[0])
            ys.append(step[1])
            zs.append(result.function.evaluate(step))

        ax.scatter(xs, ys, zs, marker='x', color='red', s=500)

    def _plot_optimum_place(self, result, ax):
        xs = [result.optimum[0]]
        ys = [result.optimum[1]]
        zs = [result.function.evaluate(result.optimum)]
        ax.scatter(xs, ys, zs, marker='o', color='blue', s=1000)

    def _function_at_xy(self, x, y, function):        
            Z = []
            for a, b in zip(x, y):
                local = []
                for c, d in zip(a, b):
                    local.append(function.evaluate([c, d]))
                Z.append(local)
            return np.array(Z)    