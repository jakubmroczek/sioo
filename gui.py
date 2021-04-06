from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog, QGridLayout, QLineEdit,
                             QPushButton)
import numpy as np
from PyQt5 import QtCore
import pyqtgraph as pg
from program_arguments import ProgramArguments, OptimizerType
from function import FunctionRange

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

        #
        self.functionLabel = QLineEdit('function')
        self.functionLowPointLabel = QLineEdit('domain start')
        self.functionHighLabel = QLineEdit('domain end')
        self.optimizerComboBox = QComboBox()
        self.optimizerComboBox.addItems([self.BISECTION, self.GOLDEN_SECTION_SEARCH, self.SCIPY_BISECTION, self.SCIPTY_GOLDEN_SECITION_SEARCH])
        self.runButton = QPushButton('Calculate!')

        layout = QGridLayout()
        layout.addWidget(self.functionLabel, 0, 0, 1, 2)
        layout.addWidget(self.functionLowPointLabel, 1, 0, 1, 2)
        layout.addWidget(self.functionHighLabel, 2, 0, 1, 2)
        layout.addWidget(self.optimizerComboBox, 3, 0, 1, 2)
        layout.addWidget(self.runButton, 4, 0, 1, 2)
        layout.addWidget(self.graphWidget, 5, 0, 1, 2)

        layout.setRowStretch(5, 1)

        self.setLayout(layout)

        # Calculation start callback
        self.onCalculationStartCallback = None

        # Assigning callbacks on click
        self.runButton.clicked.connect(self._onCalculationStart)

    def setOnCalculationStart(self, callback):
        self.onCalculationStartCallback = callback

    def _onCalculationStart(self):
        programArguments = self._getProgramArguments()
        result = self.onCalculationStartCallback(programArguments)
        self._plot(result)

    def _plot(self, result):
        self.graphWidget.clear()
        self._plot_function(result)
        self._plot_end_interval(result)
        self._plot_intermediate_intervals(result)

    def _plot_function(self, result):
        step = 0.01
        x = np.arange(result.interval.low, result.interval.high, step)
        y = [result.function.evalute(x) for x in x]

        pen = pg.mkPen(color=(255, 0, 0), width=7, style=QtCore.Qt.DashLine)

        # plot data: x, y values
        self.graphWidget.plot(x, y, pen=pen)

    def _plot_end_interval(self, result):
        x = [result.minimum_end_interval.low, result.minimum_end_interval.high]
        y = [result.function.evalute(x) for x in x]
        pen = pg.mkPen(width=0)
        self.graphWidget.plot(x, y, pen=pen, symbol='+', symbolSize=30, symbolBrush=('b'))

    def _plot_intermediate_intervals(self, result):
        pass

    def _plot_unimodality_interval(self, result):
        pass

    def _getProgramArguments(self):
        arguments = ProgramArguments()
        arguments.expression = self.functionLabel.text()
        arguments.functionRange = FunctionRange(float(self.functionLowPointLabel.text()),
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

        return arguments
