from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog, QGridLayout, QLineEdit,
                             QPushButton, QLabel)
import numpy as np
from PyQt5 import QtCore
import pyqtgraph as pg
from program_arguments import ProgramArguments, OptimizerType
from function import FunctionInterval

class GUI(QDialog):
    BISECTION = 'Bisection'
    GOLDEN_SECTION_SEARCH = 'Golden-section search'
    SCIPY_BISECTION = 'SciPy Bisection'
    SCIPTY_GOLDEN_SECITION_SEARCH = 'Sci-Py Golden-section search'

    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)

        self.originalPalette = QApplication.palette()
        self.setWindowTitle("SIOO")

        # Plot
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground('#7C7C7C')
        self.graphWidget.showGrid(x = True, y = True, alpha = 0.8)

        self.functionLabel = QLineEdit('x ** 2 - 2 * x - 10')
        self.functionLowPointLabel = QLineEdit('-1.0')
        self.functionHighLabel = QLineEdit('6.0')
        self.optimizerComboBox = QComboBox()
        self.optimizerComboBox.addItems([self.BISECTION, self.GOLDEN_SECTION_SEARCH, self.SCIPY_BISECTION, self.SCIPTY_GOLDEN_SECITION_SEARCH])
        self.runButton = QPushButton('Calculate!')

        # Line edit for iterations and xtol
        self.maxIterationsEdit = QLineEdit('5000')
        self.xtolEdit = QLineEdit('1e-5')

        functionLabel = QLabel('Function:')
        intervalStartLabel = QLabel('Interval start:')
        intervalEndLabel = QLabel('Interval end:')
        maxIterationsLabel = QLabel('Max iterations:')
        xtolLabel = QLabel('Xtol:')

        layout = QGridLayout()
        layout.addWidget(functionLabel, 0, 0, 1, 1)
        layout.addWidget(self.functionLabel, 0, 1, 1, 1)

        layout.addWidget(intervalStartLabel, 1, 0, 1, 1)
        layout.addWidget(self.functionLowPointLabel, 1, 1, 1, 1)

        layout.addWidget(intervalEndLabel, 2, 0, 1, 2)
        layout.addWidget(self.functionHighLabel, 2, 1, 1, 1)

        layout.addWidget(maxIterationsLabel, 3, 0, 1, 1)
        layout.addWidget(self.maxIterationsEdit, 3, 1, 1, 1)

        layout.addWidget(xtolLabel, 4, 0, 1, 1)
        layout.addWidget(self.xtolEdit, 4, 1, 1, 1)

        layout.addWidget(self.optimizerComboBox, 5, 0, 1, 2)
        layout.addWidget(self.runButton, 6, 0, 1, 2)
        layout.addWidget(self.graphWidget, 7, 0, 1, 2)

        layout.setRowStretch(5, 1)

        self.setLayout(layout)

        # Calculation start callback
        self.onCalculationStartCallback = None

        # Assigning callbacks on click
        self.runButton.clicked.connect(self._onCalculationStart)

    def setOnCalculationStart(self, callback):
        self.onCalculationStartCallback = callback

    def _onCalculationStart(self):
        # Clean the plot
        self.graphWidget.clear()

        programArguments = self._getProgramArguments()
        result = self.onCalculationStartCallback(programArguments)
        self._plot(result)

    def _plot(self, result):
        self.graphWidget.clear()
        self._plot_function(result)
        self._plot_unimodal_interval(result)
        self._plot_intermediate_intervals(result)
        self._plot_end_interval(result)

    def _plot_function(self, result):
        step = 0.01
        x = np.arange(result.user_interval.low, result.user_interval.high, step)
        y = [result.function.evalute(x) for x in x]

        pen = pg.mkPen(color=(255, 0, 0), width=7, style=QtCore.Qt.DashLine)

        # plot data: x, y values
        self.graphWidget.plot(x, y, pen=pen)

    def _plot_end_interval(self, result):
        pen = pg.mkPen(width=0)

        # SciPy optimzers do not return the final interval, but only a single point
        if result.minimum_end_interval != None:
            x = [result.minimum_end_interval.low, result.minimum_end_interval.high]
            y = [result.function.evalute(x) for x in x]
            self.graphWidget.plot(x, y, pen=pen, symbol='+', symbolSize=30, symbolBrush=('b'))

        x = [result.result_x]
        y = [result.function.evalute(result.result_x)]
        self.graphWidget.plot(x, y, pen=pen, symbol='+', symbolSize=40, symbolBrush=('b'))

    def _plot_intermediate_intervals(self, result):
        # The SciPy optimizers does not return the intermediate_intervals
        if result.intermediate_intervals == None:
            return

        x = []
        for interval in result.intermediate_intervals:
            x.append(interval.low)
            x.append(interval.high)
        y = [result.function.evalute(x) for x in x]
        pen = pg.mkPen(width=0)
        self.graphWidget.plot(x, y, pen=pen, symbol='x', symbolSize=15, symbolBrush=('r'))

    def _plot_unimodal_interval(self, result):
        step = 0.01
        x = np.arange(result.unimodal_interval.low, result.unimodal_interval.high, step)
        y = [result.function.evalute(x) for x in x]

        pen = pg.mkPen(color=(30, 240, 0), width=7, style=QtCore.Qt.DashLine)

        # plot data: x, y values
        self.graphWidget.plot(x, y, pen=pen)

    def _getProgramArguments(self):
        arguments = ProgramArguments()
        arguments.expression = self.functionLabel.text()
        arguments.functionInterval = FunctionInterval(float(self.functionLowPointLabel.text()),
                                                float(self.functionHighLabel.text()))

        optimzerType = str(self.optimizerComboBox.currentText())

        if optimzerType == self.BISECTION:
            arguments.optimizerType = OptimizerType.BISECTION
        elif optimzerType == self.GOLDEN_SECTION_SEARCH:
            arguments.optimizerType = OptimizerType.GOLDEN_SECTION_SEARCH
        elif optimzerType == self.SCIPY_BISECTION:
            arguments.optimizerType = OptimizerType.SCIPY_BISECTION
        else:
            arguments.optimizerType = OptimizerType.SCIPY_GOLDEN_SECTION_SEARCH

        # Max iterations
        arguments.max_iterations = int(self.maxIterationsEdit.text())

        # Xtol
        arguments.xtol = float(self.xtolEdit.text())

        return arguments
